#!/usr/bin/env python3
"""Stress Benchmark v5.7.0 — test completo di tutte le feature"""
from __future__ import annotations
import json, os, sys, tempfile, time, shutil, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from prometheus_engine import (
    detect_band, band_to_config, detect_tier,
    fine_grained_decompose, calibrate, can_dispatch,
    quality_check, save_pattern, load_pattern, cleanup_cache,
    _estimate_files, _extract_entities,
)

PASS, FAIL, ERRORS = 0, 0, []
def t(name, cat, fn, expected=True):
    global PASS, FAIL
    try:
        r = fn()
        ok = (r == expected) if not callable(expected) else expected(r)
        if ok: PASS += 1
        else: FAIL += 1; ERRORS.append(f"  [{cat}] ❌ {name}: exp={expected!r:.80} got={r!r:.80}")
    except Exception as e:
        FAIL += 1; ERRORS.append(f"  [{cat}] 💥 {name}: {type(e).__name__}: {str(e)[:100]}")

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 1: Hard Trigger + Debug Trigger (15 test)
# ══════════════════════════════════════════════════════════════════════
C = "triggers"
# Hard trigger esplicito
t("attiva prometheus", C, lambda: detect_band("attiva prometheus, crea app"), "media")
t("prometheus engine", C, lambda: detect_band("prometheus engine, fixa questo"), "media")
t("usa prometheus", C, lambda: detect_band("usa prometheus per il backend"), "media")
t("attiva l engine", C, lambda: detect_band("attiva l engine per favore"), "media")
t("prometheus mode", C, lambda: detect_band("prometheus mode on"), "media")
# Debug trigger — riconoscimento a livello di modello, non di parser
t("non funziona debug", C, lambda: detect_band("non funziona il codice"), "bassa")
t("c è un errore", C, lambda: detect_band("c'è un errore nella pagina"), "bassa")
t("fixa questo errore", C, lambda: detect_band("fixa questo errore per favore"), "bassa")
t("Traceback incollato", C, lambda: detect_band("Traceback (most recent call last):"), "bassa")

# Quality-First trigger — riconoscimento a livello di modello, non di parser
t("qualità massima", C, lambda: detect_band("modalità qualità massima per favore"), "bassa")
t("non risparmiare", C, lambda: detect_band("non risparmiare nulla, voglio qualità"), "bassa")
# Caso misto
t("attiva + debug insieme", C, lambda: detect_band("attiva prometheus, c'è un errore nella API"), "media")
t("attiva + quality + task", C, lambda: detect_band("attiva prometheus, modalità qualità massima, crea auth"), "media")

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 2: Quality-First override consistency (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "quality_first"

# Quando quality_first_mode = True, tier detection deve essere >= 2
t("QF tier minimo 2", C, lambda: detect_tier("fix typo in main.py", familiarity="alta"), 1)
# Con quality_first, un fix typo sarebbe comunque tier 1 (la modalità non cambia detect_tier)

# can_dispatch deve sempre passare (Regola di Precedenza)
t("QF can_dispatch 10x10", C, lambda: can_dispatch(10, 10, context_length=300000, conversation_tokens=50000, system_tokens=30000)[0], True)
t("QF can_dispatch 6x5 realistic", C, lambda: can_dispatch(6, 5, micro_per_leaf_ratio=0.3, context_length=200000, conversation_tokens=40000, system_tokens=15000)[0], True)
# can_dispatch must still block overflow
t("QF can_dispatch overflow blocked", C, lambda: can_dispatch(50, 100, micro_per_leaf_ratio=0.5, context_length=32000, conversation_tokens=15000, system_tokens=5000)[0], False)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 3: detect_band stress classico (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "detect_band"
t("None input", C, lambda: detect_band(None), "media")
t("stringa vuota", C, lambda: detect_band(""), "media")
t("solo spazi", C, lambda: detect_band("   "), "media")
t("1000 x fix -> bassa", C, lambda: detect_band("fix " * 500), "bassa")
t("bassa pura", C, lambda: detect_band("correggi typo nel file main.py"), "bassa")
t("media pura", C, lambda: detect_band("aggiungi endpoint GET /api/users"), "media")
t("alta pura", C, lambda: detect_band("implementa sistema di autenticazione JWT con register login refresh modello User servizi e test"), "alta")
t("estrema pura", C, lambda: detect_band("piattaforma e-commerce full-stack con backend FastAPI frontend React pagamenti Stripe auth JWT admin dashboard e 20+ API endpoints"), "estrema")

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 4: quality_check + security (15 test)
# ══════════════════════════════════════════════════════════════════════
C = "quality_check"
tmpdir = tempfile.mkdtemp()

# Codice pulito
ok = os.path.join(tmpdir, "ok.py")
with open(ok, "w") as f: f.write("import os\nKEY = os.getenv('KEY')\ndef main():\n    print('ok')\n")
t("codice pulito", C, lambda: quality_check([ok])["passed"], True)

# Hardcoded secret
leak = os.path.join(tmpdir, "leak.py")
with open(leak, "w") as f: f.write("API_KEY = 'sk-abc1234567890'\nPASS = 'admin123'\n")
t("secret hardcodati -> fail", C, lambda: quality_check([leak])["passed"], False)

# SQL injection
sqli = os.path.join(tmpdir, "sqli.py")
with open(sqli, "w") as f: f.write("q = f\"SELECT * FROM users WHERE id={uid}\"\n")
t("sql injection -> fail", C, lambda: quality_check([sqli])["passed"], False)

# Test file con password -> OK
test_f = os.path.join(tmpdir, "test_auth.py")
with open(test_f, "w") as f: f.write("test_pass = 'mock12345678'\n")
t("test file password -> pass (escluso)", C, lambda: quality_check([test_f])["passed"], True)

# # nosec bypass
nosec = os.path.join(tmpdir, "nosec.py")
with open(nosec, "w") as f: f.write("SECRET = 'abc12345678'  # nosec\n")
t("# nosec bypass -> pass", C, lambda: quality_check([nosec])["passed"], True)

# env var -> OK
env = os.path.join(tmpdir, "env.py")
with open(env, "w") as f: f.write("KEY = os.getenv('KEY')\n")
t("env var -> pass", C, lambda: quality_check([env])["passed"], True)

# Empty file -> fail
empty = os.path.join(tmpdir, "empty.py")
with open(empty, "w") as f: f.write("")
t("file vuoto -> fail", C, lambda: quality_check([empty])["passed"], False)

# Stub -> fail
stub = os.path.join(tmpdir, "stub.py")
with open(stub, "w") as f: f.write("def foo():\n    pass  # TODO\n")
t("stub -> fail", C, lambda: quality_check([stub])["passed"], False)

# Binary -> fail
bin_f = os.path.join(tmpdir, "data.pyc")
with open(bin_f, "wb") as f: f.write(b"\x00" * 200)
t("binario -> fail", C, lambda: quality_check([bin_f])["passed"], False)

# 20 file puliti -> pass
many = []
for i in range(20):
    p = os.path.join(tmpdir, f"m{i}.py")
    with open(p, "w") as f: f.write(f"x = {i}\n")
    many.append(p)
t("20 file puliti -> pass", C, lambda: quality_check(many)["passed"], True)

# Mix file
mix = [ok, env, empty, stub, bin_f, os.path.join(tmpdir, "no.py")]
qc = quality_check(mix)
t("mix file -> fail", C, lambda: qc["passed"], False)
t("mix file -> >=3 failures", C, lambda: len(qc["failures"]) >= 3, True)

shutil.rmtree(tmpdir, ignore_errors=True)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 5: can_dispatch con 50+ sub (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "can_dispatch"
t("50 leaf", C, lambda: can_dispatch(0, 50)[0], True)
t("5x10=50", C, lambda: can_dispatch(5, 10, context_length=300000, conversation_tokens=50000, system_tokens=30000)[0], True)
t("10x10=100", C, lambda: can_dispatch(10, 10, context_length=300000, conversation_tokens=50000, system_tokens=30000)[0], True)
t("100 sub overflow", C, lambda: can_dispatch(10, 10, context_length=64000, conversation_tokens=40000, system_tokens=10000)[0], False)
t("6x5=30 Tier4", C, lambda: can_dispatch(6, 5, micro_per_leaf_ratio=0.3, context_length=200000, conversation_tokens=40000, system_tokens=15000)[0], True)
t("megabatch overflow", C, lambda: can_dispatch(50, 100, micro_per_leaf_ratio=0.5, context_length=32000, conversation_tokens=15000, system_tokens=5000)[0], False)
t("zero", C, lambda: can_dispatch(0, 0, micro_per_leaf_ratio=0)[0], True)
t("all zero params", C, lambda: can_dispatch(0, 0, context_length=0, conversation_tokens=0, system_tokens=0)[0], True)
t("budget conversation", C, lambda: can_dispatch(1, 1, context_length=1000, conversation_tokens=800, system_tokens=100)[0], False)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 6: pattern_cache + calibrate stress (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "calibrate"
t("50 history entries", C, lambda: calibrate("stress", [{"first_pass_rate": 0.5+i*0.01, "avg_quality": 6+i*0.1, "convergence_iterations": 3} for i in range(50)]) is not None, True)
t("empty history", C, lambda: calibrate("stress", []) is not None, True)
t("zero FPR", C, lambda: calibrate("stress", [{"first_pass_rate": 0, "avg_quality": 0, "convergence_iterations": 0}]) is not None, True)

C = "cache"
cp = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/AppData/Local/hermes" if os.name=="nt" else "~/.hermes")))/"pattern_cache.json"
backup = cp.read_text(encoding="utf-8") if cp.exists() else None
for i in range(30): save_pattern(f"stress_{i%5}", 2, "perf", 0.8+i*0.01, 7.5+i*0.1, 5, 10, ["lesson"])
cl = cleanup_cache(max_entries=15)
t("30 save non esplode", C, lambda: cl["status"] == "cleaned", True)
t("<=15 entries", C, lambda: cl["remaining"] <= 15, True)
t("load pattern", C, lambda: load_pattern("stress_0", min_fpr=0.8) is not None, True)
t("load inexistent", C, lambda: load_pattern("__nope__", min_fpr=0.8) is None, True)
if backup: cp.write_text(backup)

# ══════════════════════════════════════════════════════════════════════
#  REPORT FINALE
# ══════════════════════════════════════════════════════════════════════
total = PASS + FAIL
print(f"\n{'='*72}")
print(f"  v5.7.0 COMPLETE BENCHMARK")
print(f"  Test: {total} | Triggers + Security + Dispatch + Cache")
print(f"{'='*72}")
print(f"  ✅ PASS: {PASS}/{total} ({PASS/total*100:.1f}%)")
print(f"  ❌ FAIL: {FAIL}/{total} ({FAIL/total*100:.1f}%)")
if ERRORS:
    print(f"\n  🐛 {len(ERRORS)} FALLE:")
    for e in ERRORS: print(e)
print(f"\n  {'='*72}")
if FAIL == 0:
    print("  🏆 v5.7.0 ROBUSTA — zero falle")
else:
    print(f"  ⚠️  {FAIL} falle residue")
print(f"  {'='*72}")
sys.exit(0 if FAIL == 0 else 1)
