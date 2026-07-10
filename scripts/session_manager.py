"""Session Manager — Long Session Support for Prometheus Engine.

Gestisce sessioni lunghe (2h+, 30+ turni) con:
- Session State File: salva su disco lo stato invece di tenerlo in context
- Checkpoint Automatico: quando context > 60%, scrive checkpoint e produce summary
- Quality Trend Monitor: rileva degradazione qualità nei turni
- Interrupt Recovery: riprende la sessione da dove era stata interrotta

Usage:
    from session_manager import SessionManager
    sm = SessionManager("build_ecommerce")
    sm.track_turn({"action": "creato modello User", "files": ["models.py"], "score": 8})
    sm.track_turn({"action": "creato routes auth", "files": ["auth.py"], "score": 7})
    if sm.should_checkpoint():
        sm.checkpoint()
    state = sm.load_latest()  # per recover dopo interrupt
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# ═══════════════════════════════════════════════════════════════════════
#  COSTANTI
# ═══════════════════════════════════════════════════════════════════════

CHECKPOINT_INTERVAL_TURNS = 8       # checkpoint ogni 8 turni
CHECKPOINT_INTERVAL_SECONDS = 600   # o ogni 10 minuti
CONTEXT_THRESHOLD_PCT = 60          # checkpoint se context > 60%
QUALITY_WINDOW_SIZE = 5             # ultimi 5 task per trend
MAX_STORED_TURNS = 3               # solo ultimi 3 turni dettagliati in context (il resto su disco)
QUALITY_DEGRADE_THRESHOLD = 15      # se qualità cala di 15% → rallenta
MAX_SESSION_FILES = 20              # massimo session file nel vault


def _sessions_dir() -> Path:
    """Ritorna il path della directory sessions cross-platform."""
    base = os.environ.get("HERMES_SESSIONS_DIR",
        os.path.expanduser("~/AppData/Local/hermes/sessions" if os.name == "nt" else "~/.hermes/sessions"))
    return Path(base)


# ═══════════════════════════════════════════════════════════════════════
#  SESSION MANAGER
# ═══════════════════════════════════════════════════════════════════════

class SessionManager:
    """Gestisce lo stato di una sessione di coding lunga.

    Args:
        session_id: Identificatore unico della sessione (es. "build_ecommerce_20260710").
        goal: Descrizione del goal della sessione.
        session_dir: Directory dove salvare i file di sessione (default: HERMES_SESSIONS_DIR).
    """

    def __init__(
        self,
        session_id: str,
        goal: str = "",
        session_dir: Optional[Path] = None,
    ):
        self.session_id = session_id
        self.goal = goal
        self.session_dir = session_dir or _sessions_dir()
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Stato corrente
        self.files_created: list[dict] = []      # [{path, turn, timestamp}]
        self.decisions: list[dict] = []           # [{turn, decision, reason}]
        self.turns: list[dict] = []               # [{turn, action, files, score, elapsed}]
        self.quality_scores: list[int] = []       # [8, 7, 9, ...] solo punteggi
        self.checkpoints: list[dict] = []         # checkpoint salvati
        self.metadata: dict[str, Any] = {
            "session_id": session_id,
            "goal": goal,
            "started_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "total_turns": 0,
            "avg_quality": None,
            "quality_trend": "stable",
            "status": "active",
        }

        # Carica sessione esistente se presente
        self._existing = self._find_existing()
        if self._existing:
            self._load_existing(self._existing)

    # ── Metodi pubblici ──

    def track_turn(
        self,
        action: str,
        files: Optional[list[str]] = None,
        score: Optional[int] = None,
        decision: Optional[str] = None,
        decision_reason: Optional[str] = None,
    ) -> dict:
        """Traccia un turno completato.

        Args:
            action: Cosa è stato fatto (es. "creato modello User").
            files: Lista di file modificati/creati.
            score: Quality score del task (0-10).
            decision: Decisione architetturale presa (se applicabile).
            decision_reason: Perché è stata presa quella decisione.

        Returns:
            Dict con quality trend e se è ora di fare checkpoint.
        """
        turn = {
            "turn": self.metadata["total_turns"],
            "action": action,
            "files": files or [],
            "score": score,
            "timestamp": datetime.utcnow().isoformat(),
            "elapsed_from_start": time.time(),
        }
        self.turns.append(turn)
        self.metadata["total_turns"] += 1
        self.metadata["last_activity"] = turn["timestamp"]

        # Traccia file
        for f in turn["files"]:
            if not any(c["path"] == f for c in self.files_created):
                self.files_created.append({
                    "path": f,
                    "turn": turn["turn"],
                    "timestamp": turn["timestamp"],
                })

        # Traccia decisioni
        if decision:
            self.decisions.append({
                "turn": turn["turn"],
                "decision": decision,
                "reason": decision_reason or "",
                "timestamp": turn["timestamp"],
            })

        # Traccia qualità
        if score is not None:
            self.quality_scores.append(score)
            self._update_quality_metrics()

        # Salva su disco
        self._persist()

        return self._check_triggers(action, score)

    def track_decision(self, decision: str, reason: str = ""):
        """Traccia una decisione architetturale."""
        self.decisions.append({
            "turn": self.metadata["total_turns"],
            "decision": decision,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
        })
        self._persist()

    def should_checkpoint(self) -> bool:
        """Verifica se è ora di fare un checkpoint.

        Returns:
            True se: ultimo checkpoint è a >8 turni OR >10 min fa.
        """
        return self._check_triggers("_check_", None)["should_checkpoint"]

    def checkpoint(self) -> dict:
        """Crea un checkpoint: scrive lo stato corrente con un summary.

        Returns:
            Dict con il checkpoint salvato.
        """
        summary = self._generate_summary()
        cp = {
            "checkpoint_id": len(self.checkpoints) + 1,
            "turn": self.metadata["total_turns"],
            "timestamp": datetime.utcnow().isoformat(),
            "summary": summary,
            "file_count": len(self.files_created),
            "decision_count": len(self.decisions),
            "avg_quality": self.metadata["avg_quality"],
            "quality_trend": self.metadata["quality_trend"],
        }
        self.checkpoints.append(cp)

        # Dopo il checkpoint, comprimi turns: tieni solo ultimi 3 dettagliati
        if len(self.turns) > MAX_STORED_TURNS:
            # Salva i turni compressi nel checkpoint
            cp["compressed_turns"] = self._compress_turns(self.turns[:-MAX_STORED_TURNS])
            # Tieni solo ultimi MAX_STORED_TURNS in memoria
            self.turns = self.turns[-MAX_STORED_TURNS:]

        self.metadata["last_checkpoint"] = cp["timestamp"]
        self._persist()
        return cp

    def load_latest(self) -> Optional[dict]:
        """Carica la sessione più recente per interrupt recovery.

        Returns:
            Dict con lo stato della sessione se trovata, None altrimenti.
        """
        if self._existing:
            return self._existing
        # Cerca il file più recente
        files = sorted(self.session_dir.glob(f"{self.session_id}_*.json"),
                       key=os.path.getmtime, reverse=True)
        if files:
            with open(files[0], "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def recover(self) -> dict:
        """Recupera lo stato della sessione dopo un interrupt.

        Returns:
            Dict con: status, last_turn, completed, pending, next_steps.
        """
        state = self.load_latest()
        if not state:
            return {"status": "no_session", "message": "Nessuna sessione precedente trovata."}

        # Carica lo stato
        self._load_existing(state)

        # Genera recovery info
        last_checkpoint = self.checkpoints[-1] if self.checkpoints else None
        last_turn = self.turns[-1] if self.turns else None

        return {
            "status": "recovered",
            "session_id": self.session_id,
            "goal": self.goal,
            "total_turns": self.metadata["total_turns"],
            "files_created": [f["path"] for f in self.files_created],
            "decisions_made": [d["decision"] for d in self.decisions],
            "last_checkpoint": last_checkpoint["summary"] if last_checkpoint else None,
            "last_action": last_turn["action"] if last_turn else None,
            "last_score": last_turn["score"] if last_turn else None,
            "avg_quality": self.metadata["avg_quality"],
            "quality_trend": self.metadata["quality_trend"],
            "suggestion": self._recovery_suggestion(),
        }

    def get_context_summary(self) -> str:
        """Genera un summary pronto per essere inserito nel contesto.
        Questo è ciò che si mostra all'inizio di un turno invece di tutta la cronologia.

        Returns:
            Stringa formattata con lo stato essenziale della sessione.
        """
        lines = []
        lines.append(f"=== SESSION STATE: {self.session_id} ===")
        lines.append(f"Goal: {self.goal}")
        lines.append(f"Turni completati: {self.metadata['total_turns']}")
        if self.metadata["avg_quality"] is not None:
            lines.append(f"Qualità media: {self.metadata['avg_quality']:.1f}/10 ({self.metadata['quality_trend']})")

        if self.files_created:
            files_list = [f["path"] for f in self.files_created[-8:]]  # ultimi 8
            lines.append(f"File modificati: {', '.join(files_list)}" +
                         (f" (+{len(self.files_created)-8} altri)" if len(self.files_created) > 8 else ""))

        if self.decisions:
            lines.append(f"Decisioni architetturali: {len(self.decisions)}")
            for d in self.decisions[-3:]:
                lines.append(f"  - [{d['turn']}] {d['decision']}")

        if self.checkpoints:
            last = self.checkpoints[-1]
            lines.append(f"Ultimo checkpoint: turno {last['turn']}")
            if "compressed_turns" in last:
                lines.append(f"Turni compressi: {len(last['compressed_turns'])}")

        # Quality trend alert
        trend = self.metadata.get("quality_trend", "stable")
        if trend == "degrading":
            lines.append("⚠️ ATTENZIONE: la qualità sta degradando. Semplifica i prossimi task.")

        lines.append("=" * 40)
        return "\n".join(lines)

    # ── Metodi privati ──

    def _check_triggers(self, action: str, score: Optional[int]) -> dict:
        """Verifica trigger per checkpoint e quality trend."""
        result = {
            "should_checkpoint": False,
            "quality_trend": self.metadata.get("quality_trend", "stable"),
            "alert": None,
        }

        # Checkpoint per turni
        if self.metadata["total_turns"] > 0 and self.metadata["total_turns"] % CHECKPOINT_INTERVAL_TURNS == 0:
            result["should_checkpoint"] = True

        # Checkpoint per tempo
        if self.checkpoints:
            last_cp_time = datetime.fromisoformat(self.checkpoints[-1]["timestamp"])
            elapsed = (datetime.utcnow() - last_cp_time).total_seconds()
            if elapsed > CHECKPOINT_INTERVAL_SECONDS:
                result["should_checkpoint"] = True

        # Quality degrade alert
        if self.metadata.get("quality_trend") == "degrading" and score and score < 6:
            result["alert"] = "⚠️ Qualità in calo persistente. Considera: 1) fai un checkpoint, 2) semplifica il prossimo task, 3) verifica se le decisioni architetturali sono ancora valide."

        return result

    def _update_quality_metrics(self):
        """Aggiorna le metriche di qualità (media, trend)."""
        if not self.quality_scores:
            return

        # Media
        self.metadata["avg_quality"] = sum(self.quality_scores) / len(self.quality_scores)

        # Trend: confronta ultimi QUALITY_WINDOW_SIZE con i precedenti
        if len(self.quality_scores) >= QUALITY_WINDOW_SIZE * 2:
            recent = self.quality_scores[-QUALITY_WINDOW_SIZE:]
            previous = self.quality_scores[-(QUALITY_WINDOW_SIZE * 2):-QUALITY_WINDOW_SIZE]
            avg_recent = sum(recent) / len(recent)
            avg_previous = sum(previous) / len(previous)

            delta_pct = (avg_recent - avg_previous) / avg_previous * 100 if avg_previous > 0 else 0
            if delta_pct < -QUALITY_DEGRADE_THRESHOLD:
                self.metadata["quality_trend"] = "degrading"
            elif delta_pct > QUALITY_DEGRADE_THRESHOLD:
                self.metadata["quality_trend"] = "improving"
            else:
                self.metadata["quality_trend"] = "stable"
        elif len(self.quality_scores) >= QUALITY_WINDOW_SIZE:
            # Non abbastanza dati per trend completo
            self.metadata["quality_trend"] = "stable"

    def _generate_summary(self) -> str:
        """Genera un summary testuale della sessione per il checkpoint."""
        lines = []
        lines.append(f"Sessione: {self.session_id}")
        lines.append(f"Goal: {self.goal}")
        lines.append(f"Turni: {self.metadata['total_turns']}")
        lines.append(f"File: {len(self.files_created)}")
        lines.append(f"Decisioni architetturali: {len(self.decisions)}")
        if self.metadata["avg_quality"] is not None:
            lines.append(f"Qualità media: {self.metadata['avg_quality']:.1f}/10 ({self.metadata['quality_trend']})")
        if self.decisions:
            lines.append("Decisioni chiave:")
            for d in self.decisions[-3:]:
                lines.append(f"  - {d['decision']}")
        return "\n".join(lines)

    def _compress_turns(self, turns: list[dict]) -> list[dict]:
        """Comprime una lista di turni in formato ridotto per il checkpoint."""
        compressed = []
        for t in turns:
            compressed.append({
                "turn": t["turn"],
                "action": t["action"][:80],  # tronca
                "score": t.get("score"),
                "files": t.get("files", [])[:3],  # solo primi 3 file
            })
        return compressed

    def _recovery_suggestion(self) -> str:
        """Suggerisce i prossimi passi dopo un recover."""
        if self.metadata["total_turns"] == 0:
            return "Inizia la sessione: definisci il goal e crea il primo task."

        last_turn = self.turns[-1] if self.turns else None
        if last_turn:
            return (f"Eri al turno {last_turn['turn']}: '{last_turn['action']}'. "
                    f"Qualità score: {last_turn.get('score', 'N/D')}/10. "
                    f"Carica il context_summary e prosegui con la prossima attività.")

        return "Carica il context_summary e valuta lo stato attuale."

    def _persist(self):
        """Salva lo stato corrente su disco."""
        state = {
            "session_id": self.session_id,
            "goal": self.goal,
            "metadata": self.metadata,
            "files_created": self.files_created,
            "decisions": self.decisions,
            "turns": self.turns,
            "checkpoints": self.checkpoints,
            "quality_scores": self.quality_scores,
        }
        path = self.session_dir / f"{self.session_id}_{self.metadata['total_turns']:04d}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        # Cleanup: mantieni solo ultimi MAX_SESSION_FILES
        files = sorted(self.session_dir.glob(f"{self.session_id}_*.json"),
                       key=os.path.getmtime, reverse=True)
        for old in files[MAX_SESSION_FILES:]:
            old.unlink(missing_ok=True)

    def _find_existing(self) -> Optional[dict]:
        """Cerca file di sessione esistenti per questo session_id."""
        files = sorted(self.session_dir.glob(f"{self.session_id}_*.json"),
                       key=os.path.getmtime, reverse=True)
        if files:
            try:
                with open(files[0], "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def _load_existing(self, state: dict):
        """Carica uno stato esistente."""
        self.files_created = state.get("files_created", [])
        self.decisions = state.get("decisions", [])
        self.turns = state.get("turns", [])
        self.checkpoints = state.get("checkpoints", [])
        self.quality_scores = state.get("quality_scores", [])
        self.metadata = state.get("metadata", self.metadata)
        self.goal = state.get("goal", self.goal)
        if self.goal and not state.get("goal"):
            self.metadata["goal"] = self.goal

    def __repr__(self) -> str:
        return (f"SessionManager(id={self.session_id}, turns={self.metadata['total_turns']}, "
                f"files={len(self.files_created)}, quality={self.metadata.get('avg_quality', '?'):.1f}/10)")
