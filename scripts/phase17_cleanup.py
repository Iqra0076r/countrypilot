from pathlib import Path
import re, json

ROOT = Path(__file__).resolve().parents[1]
articles = sorted(ROOT.glob("article/*/index.html"))

patterns = [
    (re.compile(r'\s*Applied to [^<]*?, this belongs under [^<]*?\.\s*(?=Confirm)'), ' '),
    (re.compile(r'\s*For readers using [^<]*? issue rather than a stand-alone rule;\s*'), ' '),
    (re.compile(r'\s*In [^<]*?treat this as part of the [^<]*? check;\s*'), ' '),
    (re.compile(r'\s*Within [^<]*?use this point when working through [^<]*?, then\s*'), ' '),
    (re.compile(r'\s*For this [^<]*? research path, the practical checkpoint is [^<]*?;\s*'), ' '),
    (re.compile(r'\s*For [^<]*?, connect this point to the [^<]*? decision and\s*'), ' '),
]

bad_markers = [
    "Applied to ",
    "For readers using ",
    "treat this as part of the",
    "research path, the practical checkpoint is",
    "use this point when working through",
    "connect this point to the",
]

changed_files = []
replacements = 0
for path in articles:
    original = path.read_text(encoding="utf-8")
    text = original
    local = 0
    for rx, repl in patterns:
        text, n = rx.subn(repl, text)
        local += n
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed_files.append(str(path.relative_to(ROOT)))
        replacements += local

remaining = {}
for marker in bad_markers:
    count = 0
    files = []
    for path in articles:
        txt = path.read_text(encoding="utf-8")
        if marker in txt:
            count += txt.count(marker)
            if len(files) < 20:
                files.append(str(path.relative_to(ROOT)))
    remaining[marker] = {"occurrences": count, "sample_files": files}

report = {
    "articles_scanned": len(articles),
    "files_changed": len(changed_files),
    "replacements": replacements,
    "remaining_markers": remaining,
    "changed_sample": changed_files[:100],
}
(ROOT / "docs" / "phase-17-cleanup-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))

left = sum(v["occurrences"] for v in remaining.values())
print(f"Targeted template markers remaining after pass: {left}")
