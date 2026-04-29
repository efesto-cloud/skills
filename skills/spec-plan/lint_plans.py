#!/usr/bin/env python3
"""
lint_plans.py — Linter for spec-plan todo/ files.

Usage:
    python scripts/lint_plans.py                          # lint all plans in todo/
    python scripts/lint_plans.py todo/path/to/plan.md     # lint a single file
    python scripts/lint_plans.py --check-links            # also verify spec file links exist
    python scripts/lint_plans.py --fix-dates              # auto-update stale updated: dates (dry-run by default)

Exit code 0 = clean, 1 = warnings found, 2 = errors found.
"""

import sys
import os
import re
import glob
import argparse
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(2)

# ── Constants ────────────────────────────────────────────────────────────────

VALID_SCOPES = {"use-case", "entity", "module", "project"}
VALID_STATUSES = {"not-started", "in-progress", "blocked", "done"}
TODO_ROOT = Path("todo")
SPEC_ROOT = Path("specs")
STALE_DAYS = 14  # warn if updated: is older than this many days

# ── Severity helpers ─────────────────────────────────────────────────────────

class Issue:
    ERROR = "ERROR"
    WARN  = "WARN"

    def __init__(self, severity, file, message):
        self.severity = severity
        self.file = file
        self.message = message

    def __str__(self):
        return f"[{self.severity}] {self.file}: {self.message}"

issues: list[Issue] = []

def error(file, msg): issues.append(Issue(Issue.ERROR, file, msg))
def warn(file, msg):  issues.append(Issue(Issue.WARN,  file, msg))

# ── Frontmatter parsing ──────────────────────────────────────────────────────

def parse_frontmatter(path: Path) -> tuple[dict | None, str]:
    """Return (frontmatter_dict, body) or (None, full_text) if no frontmatter."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].strip()
    try:
        fm = yaml.safe_load(fm_text)
        return fm or {}, body
    except yaml.YAMLError as e:
        return None, text

# ── Individual checks ────────────────────────────────────────────────────────

def check_frontmatter_present(path: Path, fm: dict | None):
    if fm is None:
        error(path, "No valid YAML frontmatter found — every plan file must have frontmatter")

def check_required_fields(path: Path, fm: dict):
    required = ["scope", "status", "spec", "blocked-by", "unblocks", "created", "updated"]
    for field in required:
        if field not in fm:
            error(path, f"Missing required frontmatter field: '{field}'")

def check_scope(path: Path, fm: dict):
    scope = fm.get("scope")
    if scope and scope not in VALID_SCOPES:
        error(path, f"Invalid scope '{scope}' — must be one of: {', '.join(sorted(VALID_SCOPES))}")

def check_status(path: Path, fm: dict):
    status = fm.get("status")
    if status and status not in VALID_STATUSES:
        error(path, f"Invalid status '{status}' — must be one of: {', '.join(sorted(VALID_STATUSES))}")

def check_done_file_exists(path: Path, fm: dict):
    """Plans with status:done should not exist — they should be deleted."""
    if fm.get("status") == "done":
        warn(path, "Status is 'done' — this plan should be deleted, not kept")

def check_blocked_consistency(path: Path, fm: dict):
    """If status is 'blocked', blocked-by must not be null."""
    status = fm.get("status")
    blocked_by = fm.get("blocked-by")
    if status == "blocked" and not blocked_by:
        error(path, "Status is 'blocked' but 'blocked-by' is null — must reference a blocking plan")
    if status != "blocked" and blocked_by:
        warn(path, f"Status is '{status}' but 'blocked-by' is set — consider setting status to 'blocked'")

def check_dates(path: Path, fm: dict):
    for field in ("created", "updated"):
        val = fm.get(field)
        if val is None:
            continue
        if not isinstance(val, (str, date)):
            error(path, f"Field '{field}' is not a valid date: {val!r}")
            continue
        try:
            if isinstance(val, str):
                d = datetime.strptime(val, "%Y-%m-%d").date()
            else:
                d = val
            if d > date.today():
                error(path, f"Field '{field}' is in the future: {d}")
        except ValueError:
            error(path, f"Field '{field}' has invalid format '{val}' — use YYYY-MM-DD")

def check_stale_updated(path: Path, fm: dict):
    val = fm.get("updated")
    if not val:
        return
    try:
        if isinstance(val, str):
            d = datetime.strptime(val, "%Y-%m-%d").date()
        else:
            d = val
        delta = (date.today() - d).days
        if delta > STALE_DAYS:
            warn(path, f"'updated' date is {delta} days ago — plan may be stale (threshold: {STALE_DAYS} days)")
    except (ValueError, TypeError):
        pass  # already caught in check_dates

def check_spec_links(path: Path, fm: dict, body: str, verify_links: bool):
    """Check that spec references in frontmatter and task lines resolve to real files."""
    if not verify_links:
        return

    # Collect spec paths from frontmatter
    spec_val = fm.get("spec")
    spec_paths = []
    if isinstance(spec_val, str) and spec_val not in (None, "null", ""):
        spec_paths.append(spec_val)
    elif isinstance(spec_val, list):
        spec_paths.extend([s for s in spec_val if s])

    for sp in spec_paths:
        p = Path(sp)
        if not p.exists():
            error(path, f"Frontmatter 'spec' points to non-existent file: {sp}")

    # Check inline task references like (specs/entities/order.md#fields)
    inline_refs = re.findall(r'\(specs/[^)]+\.md(?:#[^)]*)?\)', body)
    for ref in inline_refs:
        ref_path = ref.strip("()").split("#")[0]
        if not Path(ref_path).exists():
            warn(path, f"Task references non-existent spec file: {ref_path}")

def check_blocked_by_links(path: Path, fm: dict, verify_links: bool):
    """Check that blocked-by references resolve to real plan files."""
    if not verify_links:
        return
    blocked_by = fm.get("blocked-by")
    if not blocked_by or blocked_by == "null":
        return
    items = blocked_by if isinstance(blocked_by, list) else [blocked_by]
    for item in items:
        if item and not Path(item).exists():
            warn(path, f"'blocked-by' references non-existent plan: {item}")

def check_task_format(path: Path, body: str):
    """Warn on task lines that are missing a spec reference."""
    task_lines = [l.strip() for l in body.splitlines() if l.strip().startswith("- [ ]") or l.strip().startswith("- [x]")]
    for line in task_lines:
        # Accept (specs/...) or (`specs/...`) or plain specs/ anywhere in line
        has_ref = bool(re.search(r'[(`]specs/', line))
        if not has_ref:
            warn(path, f"Task missing spec reference: {line[:80]}")

def check_no_orphaned_notes(path: Path, body: str):
    """Warn if a > note: line appears without a preceding task."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("> note:"):
            # Check that the previous non-empty line is a task
            for j in range(i - 1, -1, -1):
                prev = lines[j].strip()
                if prev:
                    if not (prev.startswith("- [ ]") or prev.startswith("- [x]") or prev.startswith("> ")):
                        warn(path, f"Orphaned note (no preceding task) at line {i+1}: {stripped[:60]}")
                    break

# ── Per-file linting ─────────────────────────────────────────────────────────

def lint_file(path: Path, verify_links: bool):
    fm, body = parse_frontmatter(path)

    check_frontmatter_present(path, fm)
    if fm is None:
        return  # can't do further checks without frontmatter

    check_required_fields(path, fm)
    check_scope(path, fm)
    check_status(path, fm)
    check_done_file_exists(path, fm)
    check_blocked_consistency(path, fm)
    check_dates(path, fm)
    check_stale_updated(path, fm)
    check_spec_links(path, fm, body, verify_links)
    check_blocked_by_links(path, fm, verify_links)
    check_task_format(path, body)
    check_no_orphaned_notes(path, body)

# ── Discovery ────────────────────────────────────────────────────────────────

def find_all_plans() -> list[Path]:
    return sorted(Path(".").glob("todo/**/plan.md"))

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Lint spec-plan todo/ files")
    parser.add_argument("file", nargs="?", help="Specific plan file to lint (optional)")
    parser.add_argument("--check-links", action="store_true", help="Verify spec and blocked-by file paths exist on disk")
    parser.add_argument("--fix-dates", action="store_true", help="(dry-run) Show which files have stale updated: dates")
    args = parser.parse_args()

    if args.file:
        targets = [Path(args.file)]
        if not targets[0].exists():
            print(f"ERROR: File not found: {args.file}")
            sys.exit(2)
    else:
        targets = find_all_plans()
        if not targets:
            print("No plan.md files found under todo/")
            sys.exit(0)

    for path in targets:
        lint_file(path, verify_links=args.check_links)

    if args.fix_dates:
        print("\n── Stale updated: dates ──")
        for issue in issues:
            if "updated' date is" in issue.message:
                print(f"  {issue.file}")

    # Output
    errors   = [i for i in issues if i.severity == Issue.ERROR]
    warnings = [i for i in issues if i.severity == Issue.WARN]

    if not issues:
        print(f"✅  All {len(targets)} plan(s) clean.")
        sys.exit(0)

    print(f"\nLinted {len(targets)} plan(s) — {len(errors)} error(s), {len(warnings)} warning(s)\n")

    for issue in sorted(issues, key=lambda i: (i.severity, str(i.file))):
        icon = "❌" if issue.severity == Issue.ERROR else "⚠️ "
        print(f"{icon}  {issue}")

    if errors:
        sys.exit(2)
    sys.exit(1)


if __name__ == "__main__":
    main()
