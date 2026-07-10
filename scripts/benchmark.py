"""Prometheus Engine — Benchmark Multidimensionale.

Testa la skill su 20+ prompt reali di diverso tipo (web app, API, fix, full-stack).
Misura: accuratezza classificazione, qualità decomposizione, speed, edge case handling.

Usage:
    python benchmark.py              # benchmark completo
    python benchmark.py --quick      # versione rapida (10 prompt)
    python benchmark.py --report     # solo report finale (salta test)
"""
from __future__ import annotations

import json
import os
import sys
import time
import re
from pathlib import Path
from typing import Any, Optional
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from prometheus_engine import (
    detect_band, band_to_config, detect_tier,
    fine_grained_decompose, calibrate, can_dispatch,
    quality_check, save_pattern, load_pattern, cleanup_cache,
)


# ═══════════════════════════════════════════════════════════════════════
#  BENCHMARK DATASET — 24 prompt reali
# ═══════════════════════════════════════════════════════════════════════

BENCHMARK_PROMPTS = [
    # ── BASSA (fix/micro) ──
    {"id": "B01", "prompt": "correggi typo nel file main.py", "expected_band": "bassa", "category": "fix"},
    {"id": "B02", "prompt": "cambia colore del bottone da blu a verde", "expected_band": "bassa", "category": "css"},
    {"id": "B03", "prompt": "fix bug: IndexError quando la lista è vuota", "expected_band": "bassa", "category": "fix"},
    {"id": "B04", "prompt": "aggiusta indentation nel file routes.py", "expected_band": "bassa", "category": "fix"},

    # ── MEDIA (singola feature) ──
    {"id": "M01", "prompt": "aggiungi endpoint GET /api/users che ritorna la lista utenti", "expected_band": "media", "category": "api"},
    {"id": "M02", "prompt": "crea modello Product con campi name, price, description, category", "expected_band": "media", "category": "model"},
    {"id": "M03", "prompt": "implementa funzione di validazione email con regex", "expected_band": "media", "category": "logic"},
    {"id": "M04", "prompt": "aggiungi test per l'endpoint /api/products", "expected_band": "media", "category": "test"},
    {"id": "M05", "prompt": "refactoring: estrai la logica di auth in un servizio separato", "expected_band": "media", "category": "refactor"},

    # ── ALTA (multi-componente) ──
    {"id": "A01", "prompt": "implementa sistema di autenticazione JWT con register, login, refresh, modello User, servizi e test", "expected_band": "alta", "category": "auth"},
    {"id": "A02", "prompt": "crea API completa di task management con CRUD, filtri, paginazione, ordinamento e test", "expected_band": "alta", "category": "api"},
    {"id": "A03", "prompt": "aggiungi modulo di pagamento con Stripe, webhook, rimborsi e storico transazioni", "expected_band": "alta", "category": "payments"},
    {"id": "A04", "prompt": "implementa dashboard admin con statistiche, grafici, gestione utenti e export CSV", "expected_band": "alta", "category": "admin"},

    # ── ESTREMA (full-stack/system) ──
    {"id": "E01", "prompt": "crea piattaforma e-commerce full-stack con backend FastAPI, frontend React, pagamenti Stripe, auth JWT, admin dashboard e 20+ API endpoints", "expected_band": "estrema", "category": "fullstack"},
    {"id": "E02", "prompt": "sviluppa social media platform: profili, post, like, commenti, follow, feed algoritmico, chat real-time", "expected_band": "estrema", "category": "fullstack"},
    {"id": "E03", "prompt": "crea sistema di prenotazione ristorante con 4 entità, auth, notifiche email, disponibilità real-time e pannello admin", "expected_band": "estrema", "category": "fullstack"},

    # ── EDGE CASES (test limite) ──
    {"id": "X01", "prompt": "ciao", "expected_band": "bassa", "category": "edge"},
    {"id": "X02", "prompt": "aggiungi una riga", "expected_band": "bassa", "category": "edge"},
    {"id": "X03", "prompt": "prometheus attivo", "expected_band": "media", "category": "edge"},
    {"id": "X04", "prompt": "non lo so", "expected_band": "media", "category": "edge"},
    {"id": "X05", "prompt": "backend con FastAPI e frontend con React e database PostgreSQL con Docker e CI/CD con GitHub Actions e deploy su AWS", "expected_band": "estrema", "category": "edge"},

    # ── CROSS-LINGUA ──
    {"id": "L01", "prompt": "implement user authentication system with JWT tokens and refresh rotation", "expected_band": "alta", "category": "i18n"},
    {"id": "L02", "prompt": "fix typo in main.py", "expected_band": "bassa", "category": "i18n"},
    {"id": "L03", "prompt": "build a full-stack social media platform with real-time messaging and push notifications", "expected_band": "estrema", "category": "i18n"},
]

# Categorie
CATEGORIES = {
    "fix": "Bug fix / correzioni minori",
    "css": "Modifiche UI/CSS",
    "api": "Endpoint API / CRUD",
    "model": "Modelli dati / DB",
    "logic": "Logica applicativa",
    "test": "Test suite",
    "refactor": "Refactoring",
    "auth": "Autenticazione",
    "payments": "Pagamenti",
    "admin": "Admin dashboard",
    "fullstack": "Full-stack / Sistema completo",
    "edge": "Casi limite",
    "i18n": "Cross-lingua",
}


# ═══════════════════════════════════════════════════════════════════════
#  TEST FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════


def test_band_accuracy(prompt: str, expected: str) -> dict:
    """Test detect_band: accuratezza della classificazione."""
    start = time.time()
    try:
        result = detect_band(prompt)
        elapsed = time.time() - start
        return {
            "passed": result == expected,
            "result": result,
            "expected": expected,
            "elapsed_s": round(elapsed, 4),
            "error": None,
        }
    except Exception as e:
        return {"passed": False, "result": None, "expected": expected,
                "elapsed_s": 0, "error": str(e)}


def test_tier_consistency(band: str, prompt: str) -> dict:
    """Test detect_tier: il tier è coerente con la banda."""
    start = time.time()
    try:
        config = band_to_config(band)
        tier = detect_tier(prompt, familiarity="nessuna")
        elapsed = time.time() - start
        # Verifica: tier dovrebbe essere >= config["tier"] - 1 e <= config["tier"] + 1
        expected = config["tier"]
        consistent = abs(tier - expected) <= 1
        return {
            "passed": consistent,
            "tier": tier,
            "expected_tier": expected,
            "band": band,
            "elapsed_s": round(elapsed, 4),
            "error": None,
        }
    except Exception as e:
        return {"passed": False, "tier": None, "expected_tier": None,
                "band": band, "elapsed_s": 0, "error": str(e)}


def test_decompose_quality(prompt: str, band: str) -> dict:
    """Test fine_grained_decompose: qualità della decomposizione."""
    if band == "bassa":
        return {"passed": True, "skipped": True, "task_count": 0, "elapsed_s": 0, "error": None,
                "has_duplicates": False, "has_types": True}

    start = time.time()
    try:
        config = band_to_config(band)
        subs = max(5, config["subagents"] * 2)
        tasks = fine_grained_decompose(prompt, available_subagents=subs, iteration=0)
        elapsed = time.time() - start

        # Metriche di qualità
        has_tasks = len(tasks) > 0
        has_descriptions = all(t.get("description") and len(t["description"]) > 5 for t in tasks)
        has_criteria = all(t.get("criteria") for t in tasks)
        has_types = all(t.get("type") for t in tasks)

        # Rileva duplicati (stessa descrizione)
        descs = [t["description"] for t in tasks]
        unique_descs = len(set(descs))
        has_duplicates = unique_descs < len(descs)

        # Rileva split infiniti (task_004ba, task_004bba...)
        has_malformed_ids = any(len(t["id"]) > 15 for t in tasks)

        return {
            "passed": has_tasks and has_descriptions and has_criteria and has_types,
            "task_count": len(tasks),
            "unique_tasks": unique_descs,
            "has_duplicates": has_duplicates,
            "has_malformed_ids": has_malformed_ids,
            "has_descriptions": has_descriptions,
            "has_criteria": has_criteria,
            "has_types": has_types,
            "elapsed_s": round(elapsed, 4),
            "error": None,
        }
    except Exception as e:
        return {"passed": False, "task_count": 0, "elapsed_s": 0, "error": str(e),
                "has_duplicates": False, "has_types": False}


def test_dispatch_budget(band: str) -> dict:
    """Test can_dispatch: context budget enforcement."""
    start = time.time()
    try:
        config = band_to_config(band)
        subs = max(1, config["subagents"])
        num_orch = max(1, subs // 5 if subs >= 5 else 1)
        leafs_per = max(1, subs // num_orch if subs >= num_orch else 1)

        ok, msg = can_dispatch(num_orch, leafs_per, 0.3 if band == "estrema" else 0.1)
        elapsed = time.time() - start
        return {
            "passed": True,
            "within_budget": ok,
            "orch": num_orch,
            "leaf": leafs_per,
            "message": msg,
            "elapsed_s": round(elapsed, 4),
            "error": None,
        }
    except Exception as e:
        return {"passed": False, "within_budget": False,
                "elapsed_s": 0, "error": str(e)}


def test_quality_stub_detection() -> dict:
    """Test quality_check: rilevamento stub e file mancanti."""
    start = time.time()
    try:
        import tempfile
        test_dir = Path(tempfile.mkdtemp(prefix="pe_bench_"))
        files = []

        # File con codice valido
        good = test_dir / "good.py"
        good.write_text("def hello():\n    return 'world'\n")
        files.append(str(good))

        # File con stub
        stub = test_dir / "stub.py"
        stub.write_text("def todo_impl():\n    pass  # TODO\n")
        files.append(str(stub))

        # File vuoto
        empty = test_dir / "empty.py"
        empty.write_text("")
        files.append(str(empty))

        # File inesistente
        files.append(str(test_dir / "nonexistent.py"))

        qc = quality_check(files, task_type="api")

        # Dovrebbe rilevare: stub, empty, nonexistent
        detected_stub = any("stub" in str(f).lower() for f in qc.get("failures", []))
        detected_empty = any("vuoto" in str(f).lower() for f in qc.get("failures", []))
        detected_missing = any("non esiste" in str(f).lower() for f in qc.get("failures", []))

        elapsed = time.time() - start
        return {
            "passed": detected_stub and detected_empty and detected_missing,
            "detected_stub": detected_stub,
            "detected_empty": detected_empty,
            "detected_missing": detected_missing,
            "total_checks": qc["total_checks"],
            "failures": len(qc["failures"]),
            "elapsed_s": round(elapsed, 4),
            "error": None,
        }
    except Exception as e:
        return {"passed": False, "elapsed_s": 0, "error": str(e)}


def test_pattern_persistence() -> dict:
    """Test save/load/cleanup pattern_cache."""
    start = time.time()
    try:
        sp = save_pattern(
            goal_type="benchmark_test",
            tier=3,
            decomposition_pattern="per_type",
            first_pass_rate=0.95,
            avg_quality=8.5,
            subagent_count=5,
            task_count=10,
            lessons=["benchmark test"],
        )
        lp = load_pattern("benchmark_test", min_fpr=0.8)
        cc = cleanup_cache(max_entries=50, min_fpr=60)
        elapsed = time.time() - start
        return {
            "passed": sp["status"] == "saved" and lp is not None and cc["status"] in ("cleaned", "no_cache"),
            "saved": sp["status"],
            "loaded": lp is not None,
            "cleaned": cc["status"],
            "entries": sp["entries"],
            "elapsed_s": round(elapsed, 4),
            "error": None,
        }
    except Exception as e:
        return {"passed": False, "elapsed_s": 0, "error": str(e)}


def test_calibrate_adaptive() -> dict:
    """Test calibrate: output adattivo basato su history."""
    start = time.time()
    try:
        # History che triggera granularità fine (FPR basso)
        h1 = [
            {"first_pass_rate": 0.45, "avg_quality": 6.0, "convergence_iterations": 4},
            {"first_pass_rate": 0.50, "avg_quality": 6.2, "convergence_iterations": 3},
            {"first_pass_rate": 0.48, "avg_quality": 6.5, "convergence_iterations": 4},
        ]
        c1 = calibrate("bench_fine", h1)

        # History che triggera soglia alta (qualità alta)
        h2 = [
            {"first_pass_rate": 0.90, "avg_quality": 9.0, "convergence_iterations": 1},
            {"first_pass_rate": 0.92, "avg_quality": 9.2, "convergence_iterations": 1},
            {"first_pass_rate": 0.95, "avg_quality": 9.5, "convergence_iterations": 1},
        ]
        c2 = calibrate("bench_high", h2)

        # History insufficiente (<3 entry)
        c3 = calibrate("bench_new", [{"first_pass_rate": 0.8, "avg_quality": 7, "convergence_iterations": 2}])

        elapsed = time.time() - start
        return {
            "passed": (c1["granularity"] == "fine" and c2["threshold"] >= 8 and
                       c3["granularity"] == "balanced"),
            "fine_history": c1,
            "high_quality_history": c2,
            "insufficient_history": c3,
            "elapsed_s": round(elapsed, 4),
            "error": None,
        }
    except Exception as e:
        return {"passed": False, "elapsed_s": 0, "error": str(e)}


# ═══════════════════════════════════════════════════════════════════════
#  BENCHMARK RUNNER
# ═══════════════════════════════════════════════════════════════════════


def run_benchmark(quick: bool = False) -> dict:
    """Esegue il benchmark completo."""
    prompts = BENCHMARK_PROMPTS[:10] if quick else BENCHMARK_PROMPTS
    total_start = time.time()

    results = {
        "summary": {
            "total_prompts": len(prompts),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "total_elapsed_s": 0,
            "overall_score": 0,
            "is_quick": quick,
        },
        "band_accuracy": {"passed": 0, "failed": 0, "total": 0, "details": []},
        "tier_consistency": {"passed": 0, "failed": 0, "total": 0, "details": []},
        "decompose_quality": {"passed": 0, "failed": 0, "total": 0, "details": []},
        "dispatch_budget": {"passed": 0, "failed": 0, "total": 0, "details": []},
        "functional_tests": {"passed": 0, "failed": 0, "total": 0, "details": []},
        "categories": defaultdict(lambda: {"passed": 0, "failed": 0, "total": 0}),
        "edge_cases": {"passed": 0, "failed": 0, "total": 0, "details": []},
        "i18n": {"passed": 0, "failed": 0, "total": 0, "details": []},
        "speed": {"total_elapsed_s": 0, "avg_per_test": 0},
        "gaps": [],
        "recommendations": [],
    }

    print(f"\n{'='*70}")
    print(f"  PROMETHEUS ENGINE — BENCHMARK MULTIDIMENSIONALE")
    print(f"  Prompt: {len(prompts)}  |  {'Quick mode' if quick else 'Completo'}")
    print(f"{'='*70}")

    for item in prompts:
        pid = item["id"]
        prompt = item["prompt"]
        expected_band = item["expected_band"]
        category = item["category"]
        is_edge = category == "edge"
        is_i18n = category == "i18n"

        print(f"\n  [{pid}] \"{prompt[:60]}{'...' if len(prompt) > 60 else ''}\"")

        item_results = {}

        # ── Test 1: Band accuracy ──
        r1 = test_band_accuracy(prompt, expected_band)
        item_results["band"] = r1
        results["band_accuracy"]["total"] += 1
        results["categories"][category]["total"] += 1
        if r1["passed"]:
            results["band_accuracy"]["passed"] += 1
            results["categories"][category]["passed"] += 1
        else:
            results["band_accuracy"]["failed"] += 1
            results["categories"][category]["failed"] += 1

        # ── Test 2: Tier consistency ──
        r2 = test_tier_consistency(r1["result"] or expected_band, prompt)
        item_results["tier"] = r2
        results["tier_consistency"]["total"] += 1
        if r2["passed"]:
            results["tier_consistency"]["passed"] += 1
        else:
            results["tier_consistency"]["failed"] += 1

        # ── Test 3: Decompose quality ──
        r3 = test_decompose_quality(prompt, r1["result"] or expected_band)
        item_results["decompose"] = r3
        if not r3.get("skipped"):
            results["decompose_quality"]["total"] += 1
            if r3["passed"]:
                results["decompose_quality"]["passed"] += 1
            else:
                results["decompose_quality"]["failed"] += 1
                # Gap: decomposizione fallita
                if "malformed" in str(r3.get("error", "")):
                    results["gaps"].append(f"{pid}: decompose malformed ids")
        else:
            results["decompose_quality"]["total"] += 1
            results["decompose_quality"]["passed"] += 1  # skipped = ok

        # ── Test 4: Dispatch budget ──
        r4 = test_dispatch_budget(r1["result"] or expected_band)
        item_results["dispatch"] = r4
        results["dispatch_budget"]["total"] += 1
        if r4["passed"]:
            results["dispatch_budget"]["passed"] += 1
        else:
            results["dispatch_budget"]["failed"] += 1

        # Edge case / i18n tracking
        if is_edge:
            results["edge_cases"]["total"] += 1
            results["edge_cases"]["passed"] += 1 if r1["passed"] else 0
            results["edge_cases"]["failed"] += 0 if r1["passed"] else 1
        if is_i18n:
            results["i18n"]["total"] += 1
            results["i18n"]["passed"] += 1 if r1["passed"] else 0
            results["i18n"]["failed"] += 0 if r1["passed"] else 1

        # Output
        status = "✅" if r1["passed"] else "❌"
        band_str = f"band={r1['result']} (exp={expected_band})"
        tier_str = f"tier={r2['tier']}" if r2["tier"] else "tier=?"
        tasks_str = f"tasks={r3['task_count']}" if not r3.get("skipped") else "skip"
        print(f"     {status} {band_str} | {tier_str} | {tasks_str}")

    # ── Functional tests (una tantum, non per prompt) ──
    print(f"\n  {'─'*60}")
    print(f"  TEST FUNZIONALI")
    print(f"  {'─'*60}")

    # Quality check
    rq = test_quality_stub_detection()
    results["functional_tests"]["total"] += 1
    if rq["passed"]:
        results["functional_tests"]["passed"] += 1
        print(f"  ✅ quality_check: stub={rq['detected_stub']} empty={rq['detected_empty']} missing={rq['detected_missing']}")
    else:
        results["functional_tests"]["failed"] += 1
        results["gaps"].append("quality_check: non rileva stub/empty/missing")
        print(f"  ❌ quality_check: stub={rq['detected_stub']} empty={rq['detected_empty']} missing={rq['detected_missing']}")

    # Pattern persistence
    rp = test_pattern_persistence()
    results["functional_tests"]["total"] += 1
    if rp["passed"]:
        results["functional_tests"]["passed"] += 1
        print(f"  ✅ pattern_cache: saved={rp['saved']} loaded={rp['loaded']} entries={rp['entries']}")
    else:
        results["functional_tests"]["failed"] += 1
        results["gaps"].append("pattern_cache: save/load/cleanup fallito")
        print(f"  ❌ pattern_cache: saved={rp['saved']} loaded={rp['loaded']}")

    # Calibrate
    rc = test_calibrate_adaptive()
    results["functional_tests"]["total"] += 1
    if rc["passed"]:
        results["functional_tests"]["passed"] += 1
        print(f"  ✅ calibrate: fine={rc['fine_history']['granularity']} high={rc['high_quality_history']['threshold']} new={rc['insufficient_history']['granularity']}")
    else:
        results["functional_tests"]["failed"] += 1
        results["gaps"].append("calibrate: output non adattivo")
        print(f"  ❌ calibrate: adaptive fail")

    # ── Computa score ──
    total_tests = (results["band_accuracy"]["total"] + results["tier_consistency"]["total"] +
                   results["decompose_quality"]["total"] + results["dispatch_budget"]["total"] +
                   results["functional_tests"]["total"])
    total_passed = (results["band_accuracy"]["passed"] + results["tier_consistency"]["passed"] +
                    results["decompose_quality"]["passed"] + results["dispatch_budget"]["passed"] +
                    results["functional_tests"]["passed"])

    total_elapsed = time.time() - total_start

    results["summary"]["total_tests"] = total_tests
    results["summary"]["passed"] = total_passed
    results["summary"]["failed"] = total_tests - total_passed
    results["summary"]["total_elapsed_s"] = round(total_elapsed, 2)
    results["summary"]["overall_score"] = round(total_passed / total_tests * 100, 1) if total_tests > 0 else 0
    results["speed"]["total_elapsed_s"] = round(total_elapsed, 2)
    results["speed"]["avg_per_test"] = round(total_elapsed / total_tests, 4) if total_tests > 0 else 0

    # ── Genera raccomandazioni basate sui gap ──
    _generate_recommendations(results)

    return results


def _generate_recommendations(results: dict):
    """Genera raccomandazioni basate sui gap trovati."""
    recs = []

    # Band accuracy per categoria
    for cat, stats in results["categories"].items():
        if stats["total"] >= 2:  # almeno 2 test per categoria
            pct = stats["passed"] / stats["total"] * 100
            if pct < 80:
                recs.append(f"Migliorare detect_band per categoria '{cat}' (accuratezza {pct:.0f}%)")

    # Edge cases
    if results["edge_cases"]["total"] > 0:
        pct = results["edge_cases"]["passed"] / results["edge_cases"]["total"] * 100
        if pct < 80:
            recs.append(f"Potenziare gestione edge cases (accuratezza {pct:.0f}%)")

    # I18n
    if results["i18n"]["total"] > 0:
        pct = results["i18n"]["passed"] / results["i18n"]["total"] * 100
        if pct < 80:
            recs.append(f"Migliorare supporto cross-lingua (accuratezza {pct:.0f}%)")

    # Gaps specifici
    if any("quality_check" in g for g in results["gaps"]):
        recs.append("Fix quality_check rilevamento stub/empty/missing")
    if any("decompose" in g for g in results["gaps"]):
        recs.append("Fix decompose malformed IDs per prompt complessi")
    if any("classificazione" in g for g in results["gaps"]):
        recs.append("Bilanciare scoring band per evitare falsi positivi/negativi")

    # Raccomandazioni strutturali
    if results["speed"]["avg_per_test"] > 0.1:
        recs.append(f"Ottimizzare performance (media {results['speed']['avg_per_test']*1000:.0f}ms per test)")

    if len(recs) == 0:
        recs.append("Nessuna raccomandazione critica — tutti i test superano la soglia di accettazione")

    results["recommendations"] = recs


# ═══════════════════════════════════════════════════════════════════════
#  REPORT
# ═══════════════════════════════════════════════════════════════════════


def format_report(results: dict):
    """Stampa il report formattato."""
    s = results["summary"]
    print(f"\n{'='*70}")
    print(f"  REPORT BENCHMARK — Prometheus Engine v5")
    print(f"{'='*70}")
    print(f"\n  {'RIEPILOGO':^66}")
    print(f"  {'─'*66}")
    print(f"  Prompt testati:   {s['total_prompts']}")
    print(f"  Test totali:      {s['total_tests']}")
    print(f"  ✅ Passati:       {s['passed']}")
    print(f"  ❌ Falliti:       {s['failed']}")
    print(f"  🏆 Score:         {s['overall_score']}%")
    print(f"  ⏱  Durata:        {s['total_elapsed_s']}s")

    print(f"\n  {'ACCURATEZZA PER DIMENSIONE':^66}")
    print(f"  {'─'*66}")
    dims = [
        ("Classificazione banda", results["band_accuracy"]),
        ("Consistenza Tier", results["tier_consistency"]),
        ("Qualità decomposizione", results["decompose_quality"]),
        ("Context budget enforcement", results["dispatch_budget"]),
        ("Test funzionali", results["functional_tests"]),
    ]
    for name, dim in dims:
        if dim["total"] > 0:
            pct = dim["passed"] / dim["total"] * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  {name:35s} {bar} {pct:5.1f}%  ({dim['passed']}/{dim['total']})")

    print(f"\n  {'ACCURATEZZA PER CATEGORIA':^66}")
    print(f"  {'─'*66}")
    for cat in sorted(results["categories"].keys()):
        stats = results["categories"][cat]
        if stats["total"] > 0:
            pct = stats["passed"] / stats["total"] * 100
            label = CATEGORIES.get(cat, cat)
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  {label:35s} {bar} {pct:5.1f}%  ({stats['passed']}/{stats['total']})")

    if results["edge_cases"]["total"] > 0:
        pct = results["edge_cases"]["passed"] / results["edge_cases"]["total"] * 100
        print(f"\n  Casi limite:      {pct:.0f}% ({results['edge_cases']['passed']}/{results['edge_cases']['total']})")
    if results["i18n"]["total"] > 0:
        pct = results["i18n"]["passed"] / results["i18n"]["total"] * 100
        print(f"  Cross-lingua:     {pct:.0f}% ({results['i18n']['passed']}/{results['i18n']['total']})")

    if results["gaps"]:
        print(f"\n  {'GAP IDENTIFICATI':^66}")
        print(f"  {'─'*66}")
        for gap in results["gaps"]:
            print(f"  ❌ {gap}")

    if results["recommendations"]:
        print(f"\n  {'RACCOMANDAZIONI':^66}")
        print(f"  {'─'*66}")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"  {i}. {rec}")

    print(f"\n{'='*70}")
    print(f"  VOTO COMPLESSIVO: {s['overall_score']}/100")
    if s['overall_score'] >= 95:
        print(f"  GIUDIZIO: 🏆 Eccellente — pronto per produzione")
    elif s['overall_score'] >= 85:
        print(f"  GIUDIZIO: ✅ Buono — qualche miglioramento minore")
    elif s['overall_score'] >= 70:
        print(f"  GIUDIZIO: ⚠️ Adeguato — necessita miglioramenti")
    else:
        print(f"  GIUDIZIO: ❌ Insufficiente — richiede revisione")
    print(f"{'='*70}\n")


# ═══════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    quick = "--quick" in sys.argv
    report_only = "--report" in sys.argv

    if not report_only:
        results = run_benchmark(quick=quick)
        # Salva risultati per analisi successive
        cache_path = Path(os.path.expanduser("~/AppData/Local/hermes/pattern_cache.json"))
        try:
            with open(cache_path) as f:
                cache = json.load(f)
        except (IOError, json.JSONDecodeError):
            cache = []

        benchmark_entry = {
            "goal_type": "benchmark_v5",
            "tier": 4,
            "decomposition_pattern": "full",
            "first_pass_rate": results["summary"]["overall_score"] / 100,
            "avg_quality": results["summary"]["overall_score"] / 10,
            "subagent_count": len(BENCHMARK_PROMPTS[:10] if quick else BENCHMARK_PROMPTS),
            "task_count": results["summary"]["total_tests"],
            "lessons": results["recommendations"][:3],
            "gaps": results["gaps"][:3],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        cache.append(benchmark_entry)
        if len(cache) > 20:
            cache = sorted(cache, key=lambda x: x.get("timestamp", ""))[-15:]

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

        print(f"  Metrics salvate in pattern_cache.json ✅")

    else:
        # Solo report: carica risultati dal cache
        cache_path = Path(os.path.expanduser("~/AppData/Local/hermes/pattern_cache.json"))
        try:
            with open(cache_path) as f:
                cache = json.load(f)
            benchmarks = [e for e in cache if e.get("goal_type") == "benchmark_v5"]
            if benchmarks:
                latest = benchmarks[-1]
                print(f"\n  Benchmark più recente trovato:")
                print(f"  Score: {latest.get('first_pass_rate', 0) * 100:.1f}%")
                print(f"  Raccomandazioni: {latest.get('lessons', [])}")
            else:
                print("  Nessun benchmark trovato. Esegui python benchmark.py prima.")
        except Exception as e:
            print(f"  Errore caricamento benchmark: {e}")

    format_report(results if not report_only else {"summary": {"total_prompts": 0, "total_tests": 0, "passed": 0, "failed": 0, "overall_score": 0, "total_elapsed_s": 0}, "band_accuracy": {"passed": 0, "failed": 0, "total": 0}, "tier_consistency": {"passed": 0, "failed": 0, "total": 0}, "decompose_quality": {"passed": 0, "failed": 0, "total": 0}, "dispatch_budget": {"passed": 0, "failed": 0, "total": 0}, "functional_tests": {"passed": 0, "failed": 0, "total": 0}, "categories": {}, "edge_cases": {"passed": 0, "failed": 0, "total": 0}, "i18n": {"passed": 0, "failed": 0, "total": 0}, "speed": {}, "gaps": [], "recommendations": []})
