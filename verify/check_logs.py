"""Fail (exit 1) if any verification log reports a failure.

The verify scripts print their results to *_log.txt but do not all set an exit
code, so CI runs this scan afterwards. Rules, applied line by line:
  * 'FAILURES:' must be followed by 'none';
  * 'mismatches' must be followed by 0;
  * 'N fail' must have N == 0; a line starting with 'FAIL' is a failure;
Lines printing ': False' are not treated as failures: several are expected
answers (e.g. 'commutative? ... False').
"""
import pathlib, re, sys

here = pathlib.Path(__file__).resolve().parent
bad = []
logs = sorted(here.glob("*_log.txt"))
for log in logs:
    for n, line in enumerate(log.read_text(errors="replace").splitlines(), 1):
        s = line.strip()
        problems = [
            re.search(r"FAILURES:\s*(?!none)\S", s),
            re.search(r"mismatches:?\s*[1-9]", s),
            re.search(r"\b[1-9]\d*\s+fail", s),
            s.startswith("FAIL") and not s.startswith("FAILURES"),
        ]
        if any(problems):
            bad.append(f"{log.name}:{n}: {s}")
print(f"scanned {len(logs)} logs")
if not logs:
    sys.exit("no logs found: run the verify scripts first")
if bad:
    print("\n".join(bad))
    sys.exit(1)
print("no failures reported")
