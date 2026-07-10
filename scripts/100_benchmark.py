#!/usr/bin/env python3
"""Prometheus Engine — 100-Edge-Case Benchmark per scoprire FALLE.

Testa OGNI funzione del modulo con input limite, malformati, borderline.
Non testa l'happy path (già coperto) — cerca cosa SI ROMPE.

Usage:
    python scripts/100_benchmark.py
    python scripts/100_benchmark.py --verbose
"""

from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).parent))
from prometheus_engine import (
    detect_band, band_to_config, detect_tier,
    fine_grained_decompose, calibrate, can_dispatch,
    quality_check, save_pattern, load_pattern, cleanup_cache,
    _estimate_files, _extract_entities,
)

# ══════════════════════════════════════════════════════════════════════
#  TEST FRAMEWORK MINIMAL
# ══════════════════════════════════════════════════════════════════════

PASSED = 0
FAILED = 0
ERRORS = []
VERBOSE = False


def test(name: str, category: str, fn, expected: Any = True):
    """Esegue un test. fn può essere una lambda o un callable."""
    global PASSED, FAILED
    try:
        result = fn()
        ok = result == expected
        if ok:
            PASSED += 1
        else:
            FAILED += 1
            ERRORS.append(f"  [{category}] ❌ {name}: expected={expected!r}, got={result!r}")
    except Exception as e:
        FAILED += 1
        tb = traceback.format_exc()
        ERRORS.append(f"  [{category}] 💥 {name}: {type(e).__name__}: {e}")
        if VERBOSE:
            ERRORS.append(f"       {tb.split(chr(10))[-3].strip()}")


def test_exc(name: str, category: str, fn):
    """Test che si aspetta un'eccezione."""
    global PASSED, FAILED
    try:
        fn()
        FAILED += 1
        ERRORS.append(f"  [{category}] ❌ {name}: expected exception, got none")
    except Exception:
        PASSED += 1


# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 1: detect_band — 20 TEST
# ══════════════════════════════════════════════════════════════════════

def section1():
    cat = "detect_band"

    # 1-5: Input estremi
    test("stringa vuota", cat, lambda: detect_band(""), "media")  # default
    test("solo spazi", cat, lambda: detect_band("   "), "media")
    test("caratteri speciali puri", cat, lambda: detect_band("!@#$%^&*()_+"), "media")
    test("solo numeri", cat, lambda: detect_band("1234567890"), "media")
    test("unicode/emoji", cat, lambda: detect_band("🎉🔥🚀"), "media")

    # 6-10: Confini tra bande
    test("fix + strutturale = media?", cat, lambda: detect_band("fix api route config"))
    # "fix" + "route" = bassa 3 + media 1 → pareggio, vince più alta = media
    test("typo + struttura", cat, lambda: detect_band("fix the api endpoint please"), "media")
    test("solo 'sistema'", cat, lambda: detect_band("sistema generico qualsiasi"), "alta")
    test("frontend senza backend", cat, lambda: detect_band("crea frontend in react"), "media")
    test("50+ files senza altro", cat, lambda: detect_band("50+ files per il progetto"), "estrema")

    # 11-15: Ambiguo / borderline
    test("framework mention", cat, lambda: detect_band("usa fastapi per il backend"), "media")
    test("domanda non-coding", cat, lambda: detect_band("qual e' il senso della vita?"), "media")
    test("prompt in puro inglese tecnico", cat, lambda: detect_band("implement a simple todo app with flask"))
    # "implement" + "app" = media → check
    test("promethus (typo)", cat, lambda: detect_band("promethus attivo per favore"), "media")  # non matcha \bprometheus\b
    test("non so + struttura", cat, lambda: detect_band("non lo so come fare un sistema auth"))
    # "non lo so" +4 media, "sistema" +3 alta, "auth" +3 alta → pareggio 4 vs 6 → vince alta

    # 16-20: Casi estremi
    very_long = "crea sistema " + "con modulo " * 200
    test("prompt 200+ parole", cat, lambda: detect_band(very_long), "alta")
    test("prompt contiene codice", cat, lambda: detect_band("def foo(): pass  # crea api"), "media")
    test("maiuscolo", cat, lambda: detect_band("CREA UN SISTEMA DI AUTH COMPLETO"), "alta")
    test("ripetizione stessa parola", cat, lambda: detect_band("fix fix fix fix fix"), "bassa")
    test("stringa JSON come input", cat, lambda: detect_band('{"action": "fix", "file": "main.py"}'), "media")

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 2: band_to_config — 5 TEST
# ══════════════════════════════════════════════════════════════════════

def section2():
    cat = "band_to_config"

    test("banda inesistente -> fallback media", cat, lambda: band_to_config("super_alta")["tier"], 2)
    test("bassa -> tier=1,load=False", cat, lambda: (band_to_config("bassa")["tier"], band_to_config("bassa")["load_skill"]), (1, False))
    test("media -> tier=2,subagents=1", cat, lambda: band_to_config("media")["subagents"], 1)
    test("alta -> tier=3,subagents=5", cat, lambda: band_to_config("alta")["subagents"], 5)
    test("estrema -> tier=4,subagents=30", cat, lambda: band_to_config("estrema")["subagents"], 30)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 3: detect_tier — 15 TEST
# ══════════════════════════════════════════════════════════════════════

def section3():
    cat = "detect_tier"

    # Familiarity override edge cases
    test("familiarity inesistente -> 0 (nessuna)", cat, lambda: detect_tier("fix typo", familiarity="sconosciuta"), 1)
    test("familiarity vuota -> nessuna", cat, lambda: detect_tier("fix typo", familiarity=""), 1)

    # Stima file con input limite
    test("_estimate_files stringa vuota", cat, lambda: _estimate_files(""), 1)
    test("_estimate_files solo stop words", cat, lambda: _estimate_files("the and or but for"), 1)
    test("_estimate_files tutti i match", cat, lambda: _estimate_files("model route endpoint component test service schema migration auth login"), 4)

    # Override familiarità
    test("alta familiarità - tier non va sotto 1", cat, lambda: detect_tier("fix", familiarity="alta"), 1)
    test("alta familiarità su task grosso", cat, lambda: detect_tier("sistema prenotazione con auth notifiche email admin", familiarity="alta"))
    # files: sistema(+3), auth(+3), notifiche(+2), admin=nope... auth matchato? check...
    test("media familiarità riduce di 1", cat, lambda: detect_tier("api CRUD completo", familiarity="media"))
    # api+completo: files=api=2, auth no, frontend/backend no → ~2 → tier 1 normalmente
    # con media → -1 → tier 1

    # repo_scan edge cases
    test("repo_scan vuoto dict", cat, lambda: detect_tier("sistema auth", repo_scan={}))
    # files: auth+3, api? no → ~3 → tier 2

    test("repo_scan con import_count negativo", cat, lambda: detect_tier("fix", repo_scan={"import_count": -5, "external_integrations": 0}))
    # complexity = 1 + (-5*0.5) + 0 = 1 - 2.5 = -1.5 → <=2 → tier 1

    test("repo_scan external_apis enorme", cat, lambda: detect_tier("fix", repo_scan={"import_count": 0, "external_integrations": 100}))
    # complexity = 1 + 0 + 200 = 201 → tier 4

    # Consistency: band vs tier
    test("band=bassa -> tier dovrebbe essere 1", cat, lambda: detect_tier("correggi typo nel file", familiarity="nessuna"), 1)
    test("band=estrema -> tier >= 3", cat, lambda: detect_tier("piattaforma e-commerce full-stack con backend frontend deploy docker 50+ files", familiarity="nessuna") >= 3, True)

    # _estimate_files: combinatorics
    test("_estimate files full+stack -> +15", cat, lambda: _estimate_files("full stack app"), 16)
    test("_estimate files e-commerce -> +10", cat, lambda: _estimate_files("e-commerce platform"), 11)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 4: fine_grained_decompose — 15 TEST
# ══════════════════════════════════════════════════════════════════════

def section4():
    cat = "decompose"

    test("zero subagenti", cat, lambda: len(fine_grained_decompose("crea api", available_subagents=0)) >= 1, True)
    test("subagenti negativi", cat, lambda: len(fine_grained_decompose("crea api", available_subagents=-5)) >= 1, True)
    test("subagenti enormi (1000)", cat, lambda: len(fine_grained_decompose("crea api", available_subagents=1000)) <= 1000, True)

    # iteration edge cases
    test("iteration negativa -> 0", cat, lambda: len(fine_grained_decompose("crea api", available_subagents=5, iteration=-5)) >= 1, True)
    test("gaps=None con iter>0 -> lista vuota", cat, lambda: fine_grained_decompose("crea api", available_subagents=5, iteration=2, gaps=None), [])
    test("gaps=[] con iter>0 -> lista vuota", cat, lambda: fine_grained_decompose("crea api", available_subagents=5, iteration=2, gaps=[]), [])

    # _extract_entities edge cases
    test("_extract vuoto -> fallback 1 task generico", cat, lambda: len(_extract_entities("")), 1)
    test("_extract full stack -> auth + frontend + backend", cat, lambda: len(_extract_entities("full-stack app con auth e frontend react")) >= 3, True)
    test("_extract tutte entità -> 10+ entità", cat, lambda: len(_extract_entities("model route endpoint test component auth db migration payment admin email docker deploy ci cd")), 10)

    # Saturation: split fino a target
    test("split saturation non va in loop infinito", cat, lambda: len(fine_grained_decompose("fix typo", available_subagents=50)) <= 50, True)
    test("split genera id univoci", cat, lambda: (
        tasks := fine_grained_decompose("crea sistema auth con model route test", available_subagents=30),
        len(tasks) == len(set(t["id"] for t in tasks))
    ), True)

    # Quality criteria per tipo
    test("quality criteria per api", cat, lambda: "status_codes" in fine_grained_decompose("crea api endpoint", available_subagents=5)[0]["criteria"], True)
    test("quality criteria per test", cat, lambda: "coverage" in fine_grained_decompose("test suite", available_subagents=5)[0]["criteria"], True)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 5: quality_check — 10 TEST
# ══════════════════════════════════════════════════════════════════════

def section5():
    cat = "quality_check"

    # File inesistenti
    test("file_created vuoto -> passed", cat, lambda: quality_check([])["passed"], True)
    test("file inesistente -> failure", cat, lambda: quality_check(["/tmp/__nonexistent_path_xyz__.py"])["passed"], False)

    # Crea file temporanei per test
    tmpdir = tempfile.mkdtemp()
    good_py = os.path.join(tmpdir, "good.py")
    with open(good_py, "w") as f: f.write("x = 1\nprint(x)\n")

    stub_py = os.path.join(tmpdir, "stub.py")
    with open(stub_py, "w") as f: f.write("def foo():\n    pass\n")

    empty_py = os.path.join(tmpdir, "empty.py")
    with open(empty_py, "w") as f: f.write("")

    syntax_err = os.path.join(tmpdir, "syntax_err.py")
    with open(syntax_err, "w") as f: f.write("def foo(:\n")

    binary = os.path.join(tmpdir, "data.pyc")
    with open(binary, "wb") as f: f.write(b"\x00" * 100)

    test("file buono -> pass", cat, lambda: quality_check([good_py])["passed"], True)
    test("stub TODO/pass -> fail", cat, lambda: quality_check([stub_py])["passed"], False)
    test("file vuoto -> fail", cat, lambda: quality_check([empty_py])["passed"], False)
    test("sintassi errata -> fail", cat, lambda: quality_check([syntax_err])["passed"], False)
    test("file binario -> no crash", cat, lambda: quality_check([binary])["passed"], False)

    # check disabilitati
    test("check_stub=False", cat, lambda: quality_check([stub_py], check_stub=False)["passed"], True)
    test("check_syntax=False su .pyc", cat, lambda: quality_check([binary], check_syntax=False, check_stub=False)["passed"], False)  # esiste ma è binario

    # Pulisci
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 6: pattern_cache — 15 TEST
# ══════════════════════════════════════════════════════════════════════

def section6():
    cat = "pattern_cache"

    # Backup cache esistente
    cache_path = Path(os.environ.get("HERMES_HOME",
        os.path.expanduser("~/AppData/Local/hermes" if os.name == "nt" else "~/.hermes"))) / "pattern_cache.json"
    backup = None
    if cache_path.exists():
        backup = cache_path.read_text(encoding="utf-8")

    # 1-3: load con cache inesistente
    if cache_path.exists():
        cache_path.rename(cache_path.with_suffix(".json.bak"))
    test("load senza cache -> None", cat, lambda: load_pattern("test", min_fpr=0.8) is None, True)
    test("cleanup senza cache -> no_cache", cat, lambda: cleanup_cache()["status"], "no_cache")
    if backup:
        cache_path.write_text(backup)

    # 4-7: cache corrotta
    test("save basic", cat, lambda: save_pattern("bench_test", 2, "per_file", 0.9, 8.5, 3, 5, ["lesson1"])["status"], "saved")
    # Corrompi cache
    with open(cache_path, "w") as f: f.write("{corrotto: json,}")
    test("load cache corrotta -> None", cat, lambda: load_pattern("bench_test") is None, True)
    test("cleanup cache corrotta -> error", cat, lambda: cleanup_cache()["status"], "error")

    # 8-10: save ripristina
    test("save dopo corruzione -> saved", cat, lambda: save_pattern("bench_test_2", 1, "direct", 1.0, 10.0, 0, 1, ["ok"])["status"], "saved")

    # 11-13: load pattern matching
    test("load pattern esistente", cat, lambda: load_pattern("bench_test_2", min_fpr=0.8) is not None, True)
    test("load pattern con FPR troppo alto -> None", cat, lambda: load_pattern("bench_test_2", min_fpr=0.99) is None, True)
    test("load pattern inesistente -> None", cat, lambda: load_pattern("__never_saved__", min_fpr=0.8) is None, True)

    # 14: cleanup non rimuove entry buone
    test("cleanup non rimuove con poche entry", cat, lambda: cleanup_cache(max_entries=50)["removed"], 0)

    # 15: cleanup rimuove 3+ entry low-FPR
    for i in range(3):
        save_pattern("low_fpr_type", 1, "direct", 0.3 + i*0.05, 5.0, 1, 1, ["bad lesson"])
    test("cleanup rimuove goal_type con 3 entry <60%FPR", cat, lambda: cleanup_cache(max_entries=50)["removed"] >= 3, True)

    # Ripristina backup
    if backup:
        cache_path.write_text(backup)

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 7: calibrate — 10 TEST
# ══════════════════════════════════════════════════════════════════════

def section7():
    cat = "calibrate"

    test("history=None -> balanced, threshold=7", cat, lambda: calibrate("test", None)["granularity"], "balanced")
    test("history=[] -> balanced, threshold=7", cat, lambda: calibrate("test", [])["granularity"], "balanced")
    test("history 1 entry -> balanced (sotto 3)", cat, lambda: calibrate("test", [{"first_pass_rate": 0.5, "avg_quality": 7, "convergence_iterations": 3}])["granularity"], "balanced")
    test("history 2 entry -> balanced (sotto 3)", cat, lambda: calibrate("test", [{"first_pass_rate": 0.5, "avg_quality": 7, "convergence_iterations": 3}, {"first_pass_rate": 0.6, "avg_quality": 7, "convergence_iterations": 2}])["granularity"], "balanced")

    # 3 entries low FPR
    history_low = [
        {"first_pass_rate": 0.5, "avg_quality": 7, "convergence_iterations": 3},
        {"first_pass_rate": 0.55, "avg_quality": 7, "convergence_iterations": 3},
        {"first_pass_rate": 0.48, "avg_quality": 6.5, "convergence_iterations": 4},
    ]
    test("3 entries, FPR medio < 0.6 -> fine", cat, lambda: calibrate("test", history_low)["granularity"], "fine")
    test("FPR<0.6 -> threshold 6.5", cat, lambda: calibrate("test", history_low)["threshold"], 6.5)

    # 3 entries high quality
    history_high = [
        {"first_pass_rate": 0.9, "avg_quality": 9, "convergence_iterations": 1},
        {"first_pass_rate": 0.92, "avg_quality": 9.2, "convergence_iterations": 1},
        {"first_pass_rate": 0.95, "avg_quality": 9.5, "convergence_iterations": 1},
    ]
    test("3 entries, q>8.5 & FPR>0.85 -> balanced", cat, lambda: calibrate("test", history_high)["granularity"], "balanced")
    test("3 entries, q>8.5 -> threshold 8", cat, lambda: calibrate("test", history_high)["threshold"], 8)

    # Edge: FPR exactly at boundaries
    test("FPR esattamente 0.6 -> balanced", cat, lambda: calibrate("test", [
        {"first_pass_rate": 0.6, "avg_quality": 7, "convergence_iterations": 2},
        {"first_pass_rate": 0.6, "avg_quality": 7, "convergence_iterations": 2},
        {"first_pass_rate": 0.6, "avg_quality": 7, "convergence_iterations": 2},
    ])["granularity"], "balanced")  # 0.6 non < 0.6, quindi non va in "fine"

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 8: can_dispatch — 10 TEST
# ══════════════════════════════════════════════════════════════════════

def section8():
    cat = "can_dispatch"

    test("zero orchestratori -> OK", cat, lambda: can_dispatch(0, 5)[0], True)
    test("numeri negativi -> gestito?", cat, lambda: can_dispatch(-1, 5)[0], True)  #  -1*1500 + -1*5*500 + ... = negativo → dentro budget
    test("orchestrator=0, leaf=0 -> OK", cat, lambda: can_dispatch(0, 0)[0], True)
    test("context_length=0 -> overflow", cat, lambda: can_dispatch(5, 10, context_length=0)[0], False)
    test("conversation_tokens > context -> overflow", cat, lambda: can_dispatch(1, 1, context_length=1000, conversation_tokens=5000)[0], False)

    # Budget boundary
    test("budget esattamente consumato -> OK", cat, lambda: can_dispatch(1, 2, micro_per_leaf_ratio=0, context_length=5000, conversation_tokens=1000, system_tokens=500)[0], True)
    # 1*1500 + 1*2*500 + 0 = 2500. budget = (5000-1000-500)*0.4 = 3500*0.4 = 1400 → overflow!

    test("budget esattamente consumato v2", cat, lambda: can_dispatch(1, 1, micro_per_leaf_ratio=0, context_length=10000, conversation_tokens=1000, system_tokens=500)[0], True)
    # 1*1500 + 1*1*500 = 2000. budget = (10000-1000-500)*0.4 = 8500*0.4 = 3400 → OK

    test("micro_per_leaf_ratio=1.0", cat, lambda: can_dispatch(2, 3, micro_per_leaf_ratio=1.0)[0], True)
    test("tutti zero", cat, lambda: can_dispatch(0, 0, context_length=0, conversation_tokens=0, system_tokens=0)[0], True)
    test("valori realistici grandi", cat, lambda: can_dispatch(10, 20, micro_per_leaf_ratio=0.3, context_length=128_000, conversation_tokens=50_000, system_tokens=20_000)[0], True)
    # 10*1500=15000, 10*20*500=100000, micro=15000? 200*0.3/100*2 = circa

# ══════════════════════════════════════════════════════════════════════
#  SEZIONE 9: Cross-cutting — 10 TEST
# ══════════════════════════════════════════════════════════════════════

def section9():
    cat = "cross-cutting"

    # Consistenza band→tier
    test("band=bassa → tier=1", cat, lambda: detect_tier("correggi typo main.py", familiarity="nessuna"), 1)
    test("band=media → tier>=2", cat, lambda: detect_tier("aggiungi endpoint GET", familiarity="nessuna"), 2)
    test("band=estrema fittizia vs reale", cat, lambda: detect_tier("crea piattaforma e-commerce full-stack con backend frontend deploy docker pagamenti", familiarity="nessuna") >= 3, True)

    # Familiarità riduce drammaticamente
    test("alta familiarità su task enorme -> tier basso", cat, lambda: detect_tier("crea piattaforma e-commerce full-stack con backend frontend deploy docker 50+ files pagamenti auth admin dashboard", familiarity="alta"))
    # base: files~30 → tier 4. alta=-2 → tier 2

    # Pipeline completa: save→load→calibrate
    test("pipeline save→load→calibrate", cat, lambda: (
        save_pattern("pipe_test", 2, "per_file", 0.85, 8.0, 3, 5, ["pipe lesson"]),
        loaded := load_pattern("pipe_test", min_fpr=0.8),
        loaded is not None and calibrate("pipe_test", [loaded])["threshold"] in (7, 8)
    ), True)

    # _estimate_files non crasha su input bizzarri
    test("_estimate files con null byte", cat, lambda: _estimate_files("fix\0bug"), 1)
    test("_estimate files molto lungo", cat, lambda: _estimate_files("x " * 10000) > 0, True)

    # _extract_entities duplicati
    test("_extract entities no duplicati file", cat, lambda: (
        entities := _extract_entities("api endpoint route model test component"),
        len(set(e["files"][0] for e in entities)) == len(entities)
    ), True)

    # can_dispatch + decompose consistenza
    tasks = fine_grained_decompose("sistema auth completo", available_subagents=10)
    test("decompose tasks hanno tutti id", cat, lambda: all(t.get("id") for t in tasks), True)
    test("decompose tasks hanno tutti criteria", cat, lambda: all(t.get("criteria") for t in tasks), True)


# ══════════════════════════════════════════════════════════════════════
#  RUN ALL 100 TESTS
# ══════════════════════════════════════════════════════════════════════

def main():
    global VERBOSE, PASSED, FAILED
    VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv

    sections = [
        ("📡 detect_band (20 test)", section1),
        ("⚙️  band_to_config (5 test)", section2),
        ("📊 detect_tier (15 test)", section3),
        ("🧩 decompose (15 test)", section4),
        ("🔍 quality_check (10 test)", section5),
        ("💾 pattern_cache (15 test)", section6),
        ("📐 calibrate (10 test)", section7),
        ("🚦 can_dispatch (10 test)", section8),
        ("🔗 cross-cutting (10 test)", section9),
    ]

    print("=" * 72)
    print("  PROMETHEUS ENGINE — 100-EDGE-CASE BENCHMARK")
    print("  Scovare falle: input limite, malformati, borderline")
    print("=" * 72)

    start = time.time()

    for section_name, section_fn in sections:
        before = (PASSED, FAILED)
        try:
            section_fn()
        except Exception as e:
            FAILED += 1
            ERRORS.append(f"  💥 SEZIONE CRASHATA: {section_name}: {e}")
        done = (PASSED + FAILED) - sum(before)
        color = "✅" if FAILED == before[1] else "❌"
        print(f"\n  {color} {section_name} → {done} test completati")

    duration = time.time() - start
    total = PASSED + FAILED

    print("\n" + "=" * 72)
    print(f"  RISULTATO FINALE")
    print("=" * 72)
    print(f"  ✅ Passati:  {PASSED}/{total}")
    print(f"  ❌ Falliti:  {FAILED}/{total}")
    print(f"  ⏱  Durata:   {duration:.2f}s")
    print()

    if ERRORS:
        print("  🐛 FALLE SCOPERITE:")
        for e in ERRORS:
            print(e)
        print()

    # Calcola score
    if FAILED == 0:
        print(f"  🏆 Score: 100% — nessuna falla trovata")
    else:
        pct = PASSED / total * 100
        print(f"  🐞 Score: {pct:.1f}% — {FAILED} falle trovate!")
        print(f"  ⚠️  Questi sono bachi REALI o limiti del codice.")

    print("=" * 72)

    # Exit code
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()
