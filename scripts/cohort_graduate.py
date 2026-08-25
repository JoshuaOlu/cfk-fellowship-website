"""
cohort_graduate.py
──────────────────
Graduates Fellows from a cohort.

For each Fellow in the graduating CSV:
  1. Creates _data/fellows/[slug].yml
  2. Creates _fellows/[slug].md  (generates their profile page)

Updates the cohort Fellows list to show ONLY the graduates
(Fellows who did not graduate are removed from the cohort page).

USAGE
  python scripts/cohort_graduate.py --cohort autumn-2026 --csv graduating.csv

  # Dry run — see what would be created without writing anything
  python scripts/cohort_graduate.py --cohort autumn-2026 --csv graduating.csv --dry-run

GRADUATING CSV FORMAT
  Required columns: first_name, last_name, track
  Optional columns: vid, current_role, photo

  The script generates the slug from first_name + last_name.
  Override with a 'slug' column if needed.

WHAT HAPPENS TO NON-GRADUATES
  They are removed from the cohort Fellows list file.
  No YAML or stub file is created for them.
  They will not appear anywhere on the live site.
"""

import os
import sys
import csv
import re
import argparse

REPO_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELLOWS_DIR = os.path.join(REPO_ROOT, '_data', 'fellows')
STUBS_DIR   = os.path.join(REPO_ROOT, '_fellows')
DATA_DIR    = os.path.join(REPO_ROOT, '_data')

sys.path.insert(0, os.path.dirname(__file__))
from fellows_import import write_fellow, load_existing
from fellow_add import make_slug, create_stub

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml")
    sys.exit(1)


def load_cohort_list(cohort_slug):
    """Load the cohort Fellows list YAML."""
    filename = f"{cohort_slug}-fellows.yml"
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"ERROR: Cohort file not found: _data/{filename}")
        print(f"       Make sure the cohort slug matches exactly (e.g. 'autumn-2026').")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or []
    return path, data


def write_cohort_list(path, fellows, dry_run=False):
    """Write updated cohort Fellows list — only the graduates."""
    lines = [
        '# Updated by cohort_graduate.py — shows only Fellows who completed the cohort.',
        '# Fellows who did not graduate have been removed.',
        '',
    ]
    for f in fellows:
        lines.append(f'- first_name: "{f.get("first_name", "")}"')
        lines.append(f'  last_name: "{f.get("last_name", "")}"')
        lines.append(f'  track: "{f.get("track", "")}"')
        lines.append(f'  photo: "{f.get("photo", "")}"')
        lines.append('')

    content = '\n'.join(lines)
    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    return content


def build_fellow_data(row, cohort_slug, cohort_name):
    """Build a Fellow data dict from a graduating CSV row."""
    first = row.get('first_name', '').strip()
    last  = row.get('last_name', '').strip()
    slug  = row.get('slug', '').strip() or make_slug(first, last)

    data = {
        'slug':         slug,
        'vid':          row.get('vid', '').strip(),
        'first_name':   first,
        'last_name':    last,
        'photo':        row.get('photo', '').strip() or f"/assets/images/fellows/{slug}.jpg",
        'status':       'active',
        'level':        'Foundation Fellow',
        'track':        row.get('track', '').strip(),
        'cohort':       cohort_name,
        'joined':       cohort_name,
        'exited':       '',
        'current_role': row.get('current_role', '').strip(),
        'other_roles':  '',
        'timeline':     '',
        'bio':          '',
        'statement':    '',
        'linkedin': '', 'instagram': '', 'x': '',
        'substack': '', 'orcid': '', 'youtube': '', 'tiktok': '',
    }
    return slug, data


def main():
    parser = argparse.ArgumentParser(description='Graduate Fellows from a cohort.')
    parser.add_argument('--cohort', required=True,
                        help='Cohort slug (e.g. autumn-2026). Must match the _data/[cohort]-fellows.yml filename.')
    parser.add_argument('--csv', required=True,
                        help='CSV of graduating Fellows (first_name, last_name, track required).')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview what would be created without writing any files.')
    args = parser.parse_args()

    csv_path = args.csv if os.path.isabs(args.csv) else os.path.join(REPO_ROOT, args.csv)
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV not found: {csv_path}")
        sys.exit(1)

    # Load cohort list to get the full cohort name
    cohort_list_path, all_cohort_fellows = load_cohort_list(args.cohort)

    # Try to infer the cohort name from the slug
    parts = args.cohort.split('-')  # e.g. ['autumn', '2026']
    cohort_name = f"{parts[0].title()} {parts[1]}" if len(parts) == 2 else args.cohort

    # Load graduating CSV
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        required = ['first_name', 'last_name', 'track']
        missing = [h for h in required if h not in headers]
        if missing:
            print(f"ERROR: CSV missing required columns: {', '.join(missing)}")
            sys.exit(1)
        rows = list(reader)

    if not rows:
        print("ERROR: CSV is empty.")
        sys.exit(0)

    if args.dry_run:
        print("DRY RUN — no files will be written.\n")

    created = []
    skipped = []
    graduate_names = []  # track who graduated for cohort list update

    print(f"Graduating {len(rows)} Fellow(s) from cohort: {cohort_name}\n")

    for row in rows:
        first = row.get('first_name', '').strip()
        last  = row.get('last_name', '').strip()
        if not first or not last:
            skipped.append(f"  Row missing first_name or last_name — skipped")
            continue

        slug, data = build_fellow_data(row, args.cohort, cohort_name)

        # Check for existing Fellow
        existing = load_existing(slug)
        if existing:
            print(f"  ⚠️  {first} {last} ({slug}) already has a profile — skipping YAML creation.")
            skipped.append(f"  {slug}: already exists")
        else:
            if not args.dry_run:
                write_fellow(slug, data)
                create_stub(slug)
            created.append(slug)
            print(f"  ✅ {first} {last} → _data/fellows/{slug}.yml + _fellows/{slug}.md")

        # Track their name for cohort list
        graduate_names.append({'first_name': first, 'last_name': last,
                                'track': data['track'], 'photo': data['photo']})

    # Update the cohort list to show only graduates
    print(f"\nUpdating cohort list to show only {len(graduate_names)} graduate(s)...")
    if not args.dry_run:
        write_cohort_list(cohort_list_path, graduate_names)
        print(f"  ✅ Updated _data/{args.cohort}-fellows.yml")
    else:
        print(f"  (DRY RUN) Would update _data/{args.cohort}-fellows.yml")
        removed = len(all_cohort_fellows) - len(graduate_names)
        if removed > 0:
            print(f"  Would remove {removed} non-graduating Fellow(s) from cohort list.")

    # Summary
    print(f"\n{'─'*50}")
    print(f"  Created:  {len(created)} Fellow profile(s)")
    if skipped:
        print(f"  Skipped:  {len(skipped)}")
        for s in skipped:
            print(s)

    if not args.dry_run:
        print(f"\nNEXT STEPS:")
        print(f"  → Upload headshots to assets/images/fellows/")
        print(f"  → Send fellows the bio/statement collection form")
        print(f"  → Run: python scripts/fellows_audit.py  to see what's missing")
        print(f"  → Commit and push to GitHub")


if __name__ == '__main__':
    main()
