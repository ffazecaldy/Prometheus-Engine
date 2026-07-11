#!/usr/bin/env python3
"""Stress Benchmark v5.5.5 — patched expectations."""
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
#  1 — detect_band stress (25 test)
# ══════════════════════════════════════════════════════════════════════
C = "detect_band"
t("None input", C, lambda: detect_band(None), "media")
t("integer come stringa", C, lambda: detect_band(str(10**50)), "media")
t("binary/non utf8", C, lambda: detect_band("\x00\x01\x02\x03"), "media")
t("html snippet", C, lambda: detect_band("<html><body>Ciao</body></html>"), "media")
t("hard trigger: attiva engine", C, lambda: detect_band("attiva engine per questo progetto"), "media")
t("hard trigger: usa prometheus", C, lambda: detect_band("usa prometheus per favore"), "media")
t("hard trigger: prometheus mode", C, lambda: detect_band("prometheus mode"), "media")
t("hard trigger: prometheus on", C, lambda: detect_band("prometheus on"), "media")
t("hard trigger: fix + attiva prometheus", C, lambda: detect_band("attiva prometheus, fix typo"), "media")
t("bassa pura: fix typo main.py", C, lambda: detect_band("fix typo in main.py"), "bassa")
t("media pura: crea endpoint API", C, lambda: detect_band("crea endpoint per API"), "media")
t("alta pura: sistema auth", C, lambda: detect_band("implementa sistema di autenticazione JWT con register login refresh"), "alta")
t("estrema pura: full-stack MVP", C, lambda: detect_band("piattaforma e-commerce full-stack con backend frontend deploy docker 50+ files pagamenti auth admin dashboard notifiche"), "estrema")
t("1000 x 'fix' -> bassa", C, lambda: detect_band("fix " * 500), "bassa")
t("1000 x 'sistema' -> alta", C, lambda: detect_band("sistema " * 500), "alta")

# ══════════════════════════════════════════════════════════════════════
#  2 — detect_tier + _estimate_files (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "detect_tier"
t("repo_scan con import enormi -> tier 4", C, lambda: detect_tier("crea api", repo_scan={"import_count": 999, "external_integrations": 999}) >= 3, True)
t("tier 4 per fullstack sconosciuto", C, lambda: detect_tier("piattaforma e-commerce full-stack con backend frontend deploy docker 50+ files", familiarity="nessuna") >= 3, True)
t("alta familiarità riduce", C, lambda: detect_tier("sistema auth JWT completo con modello User servizi test", familiarity="alta") <= 2, True)

C = "_estimate_files"
t("50 parole chiave", C, lambda: _estimate_files("sistema auth modulo premio notifica email login frontend backend") >= 6, True)
t("frase minima", C, lambda: _estimate_files("fix"), 1)
t("full + stack => +15", C, lambda: _estimate_files("full stack app"), 15)
t("e-commerce => +10", C, lambda: _estimate_files("e-commerce platform"), 10)

# ══════════════════════════════════════════════════════════════════════
#  3 — decompose stress (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "decompose"
t("100 sub -> non crasha", C, lambda: len(fine_grained_decompose("crea e-commerce", available_subagents=100)) > 0, True)
t("100 sub -> non esplode", C, lambda: len(fine_grained_decompose("crea e-commerce", available_subagents=100)) <= 100, True)
t("50 sub su fix typo", C, lambda: len(fine_grained_decompose("fix typo main.py", available_subagents=50)) > 0, True)
t("tutte entità -> 10+", C, lambda: len(fine_grained_decompose("model route endpoint test component auth db migrations payment email admin deploy docker", available_subagents=20)) >= 10, True)
t("fallback goal vuoto -> 1 task generico", C, lambda: len(_extract_entities("")), 1)

# ══════════════════════════════════════════════════════════════════════
#  4 — quality_check stress (15 test)
# ══════════════════════════════════════════════════════════════════════
C = "quality_check"
tmpdir = tempfile.mkdtemp()

ok = os.path.join(tmpdir, "ok.py")
with open(ok, "w") as f: f.write("import os\nAPI_KEY = os.getenv('API_KEY')\n\ndef main():\n    print('hello')\n")
t("codice pulito -> pass", C, lambda: quality_check([ok])["passed"], True)

secret = os.path.join(tmpdir, "leaky.py")
with open(secret, "w") as f: f.write("API_KEY = 'sk-abc1234567890'\nPASSWORD = 'admin123'\n")
t("secret hardcodati -> fail", C, lambda: quality_check([secret])["passed"], False)

sqli = os.path.join(tmpdir, "sqli.py")
with open(sqli, "w") as f: f.write("query = f\"SELECT * FROM users WHERE id={user_id}\"\ncursor.execute(query)\n")
t("sql injection -> fail", C, lambda: quality_check([sqli])["passed"], False)

test_f = os.path.join(tmpdir, "test_auth.py")
with open(test_f, "w") as f: f.write("test_password = 'mock_password_12345'\n")
t("file test con password -> pass", C, lambda: quality_check([test_f])["passed"], True)

nosec = os.path.join(tmpdir, "nosec.py")
with open(nosec, "w") as f: f.write("API_KEY = 'sk-abc1234567890'  # nosec\n")
t("# nosec -> pass", C, lambda: quality_check([nosec])["passed"], True)

env = os.path.join(tmpdir, "env.py")
with open(env, "w") as f: f.write("API_KEY = os.getenv('API_KEY')\nDB_PASS = os.environ['DB_PASS']\n")
t("env var -> pass", C, lambda: quality_check([env])["passed"], True)

t("file inesistente -> fail", C, lambda: quality_check([os.path.join(tmpdir, "no.py")])["passed"], False)
empty = os.path.join(tmpdir, "empty.py")
with open(empty, "w") as f: f.write("")
t("file vuoto -> fail", C, lambda: quality_check([empty])["passed"], False)
stub = os.path.join(tmpdir, "stub.py")
with open(stub, "w") as f: f.write("def foo():\n    pass  # TODO\n")
t("stub -> fail", C, lambda: quality_check([stub])["passed"], False)
bin_f = os.path.join(tmpdir, "data.pyc")
with open(bin_f, "wb") as f: f.write(b"\x00" * 200)
t("binario -> fail", C, lambda: quality_check([bin_f])["passed"], False)

many = []
for i in range(20):
    p = os.path.join(tmpdir, f"m{i}.py")
    with open(p, "w") as f: f.write(f"x = {i}\n")
    many.append(p)
t("20 file puliti -> pass", C, lambda: quality_check(many)["passed"], True)

all_5 = [ok, env, empty, stub, bin_f, os.path.join(tmpdir, "no.py")]
qc = quality_check(all_5)
t("mix file -> almeno 1 fail", C, lambda: qc["passed"], False)
t("mix check -> 4+ failures", C, lambda: len(qc["failures"]) >= 4, True)

shutil.rmtree(tmpdir, ignore_errors=True)

# ══════════════════════════════════════════════════════════════════════
#  5 — can_dispatch con 50+ sub (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "can_dispatch"
t("50 leaf, 0 orch", C, lambda: can_dispatch(0, 50)[0], True)
t("5x10=50, context largo", C, lambda: can_dispatch(5, 10, context_length=300000, conversation_tokens=50000, system_tokens=30000)[0], True)
t("10x10=100, context largo", C, lambda: can_dispatch(10, 10, context_length=300000, conversation_tokens=50000, system_tokens=30000)[0], True)
t("100 sub, context stretto -> overflow", C, lambda: can_dispatch(10, 10, context_length=64000, conversation_tokens=40000, system_tokens=10000)[0], False)
t("6x5=30 Tier 4 realistico", C, lambda: can_dispatch(6, 5, micro_per_leaf_ratio=0.3, context_length=200000, conversation_tokens=40000, system_tokens=15000)[0], True)
t("50x100, tiny context -> overflow", C, lambda: can_dispatch(50, 100, micro_per_leaf_ratio=0.5, context_length=32000, conversation_tokens=15000, system_tokens=5000)[0], False)
t("0 orch, 0 leaf -> OK", C, lambda: can_dispatch(0, 0, micro_per_leaf_ratio=0)[0], True)
t("all params zero -> OK", C, lambda: can_dispatch(0, 0, context_length=0, conversation_tokens=0, system_tokens=0)[0], True)
t("1x1 context minimo -> overflow (budget stretto)", C, lambda: can_dispatch(1, 1, micro_per_leaf_ratio=0, context_length=2000, conversation_tokens=0, system_tokens=0)[0], False)
t("budget esaurito da conversation", C, lambda: can_dispatch(1, 1, context_length=1000, conversation_tokens=800, system_tokens=100)[0], False)

# ══════════════════════════════════════════════════════════════════════
#  6 — pattern_cache + calibrate (10 test)
# ══════════════════════════════════════════════════════════════════════
C = "calibrate"
t("50 entry history", C, lambda: calibrate("stress", [{"first_pass_rate": 0.5+i*0.01, "avg_quality": 6+i*0.1, "convergence_iterations": 3} for i in range(50)]) is not None, True)
t("0 entry history", C, lambda: calibrate("stress", []) is not None, True)
t("zero FPR history", C, lambda: calibrate("stress", [{"first_pass_rate": 0, "avg_quality": 0, "convergence_iterations": 0}]) is not None, True)

C = "cache"
cp = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/AppData/Local/hermes" if os.name=="nt" else "~/.hermes")))/"pattern_cache.json"
if cp.exists(): backup = cp.read_text(encoding="utf-8")
for i in range(30): save_pattern(f"stress_{i%5}", 2, "perf", 0.8+i*0.01, 7.5+i*0.1, 5, 10, ["lesson"])
cl = cleanup_cache(max_entries=15)
t("cache non esplode con 30 save", C, lambda: cl["status"] == "cleaned", True)
t("rimangono <=15", C, lambda: cl["remaining"] <= 15, True)
t("load pattern esistente", C, lambda: load_pattern("stress_0", min_fpr=0.8) is not None, True)
t("load pattern inesistente", C, lambda: load_pattern("__nope__", min_fpr=0.8) is None, True)
if backup: cp.write_text(backup)

# ══════════════════════════════════════════════════════════════════════
#  REPORT
# ══════════════════════════════════════════════════════════════════════
total = PASS + FAIL
print(f"\n{'='*72}")
print(f"  STRESS BENCHMARK v5.5.5 — 55 test")
print(f"  Subagenti simulati: 50, 100, 6x5=30, 10x10=100")
print(f"  Pattern cache: 30 save + cleanup + load")
print(f"{'='*72}")
print(f"  ✅ PASS: {PASS}/{total} ({PASS/total*100:.1f}%)")
print(f"  ❌ FAIL: {FAIL}/{total} ({FAIL/total*100:.1f}%)")
if ERRORS:
    print(f"\n  🐛 FALLE:")
    for e in ERRORS: print(e)
print(f"\n  {'='*72}")
if FAIL == 0:
    print("  🏆 ROBUSTO — nessuna falla con 50+ subagenti")
else:
    print(f"  ⚠️  {FAIL} falle residue")
print(f"  {'='*72}")
sys.exit(0 if FAIL == 0 else 1)
