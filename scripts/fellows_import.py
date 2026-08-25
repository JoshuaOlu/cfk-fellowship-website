"""
fellows_import.py
─────────────────
Imports a CSV and creates or updates Fellow YAML files.

The --fields flag controls which columns are written. Fields not listed
are left exactly as they are in the existing YAML. This is the safety
mechanism — a blank cell in the CSV will NOT overwrite existing data
unless that field is explicitly included in --fields.

The script verifies all required column headers before doing anything.

USAGE
  # Update only bio, statement, and social links for existing Fellows
  python scripts/fellows_import.py --csv collected_details.csv --fields bio,statement,linkedin,instagram,x,substack,orcid,youtube,tiktok

  # Full import — create or fully overwrite Fellow files
  python scripts/fellows_import.py --csv new_fellows.csv --full

  # Dry run — see what would change without writing anything
  python scripts/fellows_import.py --csv collected_details.csv --fields bio,statement --dry-run

REQUIRED CSV COLUMNS
  slug is always required (it identifies which Fellow to update).
  All other columns depend on what you pass to --fields.

STANDARD CSV COLUMN NAMES
  slug, vid, first_name, last_name, photo, status, level, track,
  cohort, joined, exited, current_role, other_roles, timeline,
  bio, statement, linkedin, instagram, x, substack, orcid, youtube, tiktok

  other_roles and timeline: semicolon-separated within a single cell
  e.g.  "RMC Team Lead; Model NASS Steering Committee"
"""

import os
import sys
import csv
import argparse
import shutil
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELLOWS_DIR = os.path.join(REPO_ROOT, '_data', 'fellows')

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml")
    sys.exit(1)

ALL_COLUMNS = [
    'slug', 'vid', 'first_name', 'last_name', 'photo',
    'status', 'level', 'track', 'cohort', 'joined', 'exited',
    'current_role', 'other_roles', 'timeline',
    'bio', 'statement',
    'linkedin', 'instagram', 'x', 'substack', 'orcid', 'youtube', 'tiktok',
]

LIST_FIELDS = {'other_roles', 'timeline'}


def load_existing(slug):
    """Load existing Fellow YAML, return empty dict if not found."""
    path = os.path.join(FELLOWS_DIR, f'{slug}.yml')
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    return data


def write_fellow(slug, data, dry_run=False):
    """Write a Fellow YAML file."""
    path = os.path.join(FELLOWS_DIR, f'{slug}.yml')

    # Build YAML content with comments
    lines = [
        f'# ── IDENTITY ─────────────────────────────────────',
        f'vid: "{data.get("vid", "")}"',
        f'slug: "{slug}"',
        f'first_name: "{data.get("first_name", "")}"',
        f'last_name: "{data.get("last_name", "")}"',
        f'photo: "{data.get("photo", "")}"',
        f'',
        f'# ── FELLOWSHIP STATUS ─────────────────────────────',
        f'status: "{data.get("status", "active")}"',
        f'level: "{data.get("level", "Foundation Fellow")}"',
        f'track: "{data.get("track", "")}"',
        f'cohort: "{data.get("cohort", "")}"',
        f'joined: "{data.get("joined", "")}"',
        f'exited: "{data.get("exited", "")}"',
        f'',
        f'# ── CONTRIBUTION RECORD ───────────────────────────',
        f'current_role: "{data.get("current_role", "")}"',
    ]

    # other_roles
    other_roles = data.get('other_roles', [])
    if isinstance(other_roles, str):
        other_roles = [r.strip() for r in other_roles.split(';') if r.strip()]
    if other_roles:
        lines.append('other_roles:')
        for role in other_roles:
            lines.append(f'  - "{role}"')
    else:
        lines.append('other_roles: []')

    # timeline
    timeline = data.get('timeline', [])
    if isinstance(timeline, str):
        timeline = [t.strip() for t in timeline.split(';') if t.strip()]
    if timeline:
        lines.append('timeline:')
        for entry in timeline:
            lines.append(f'  - "{entry}"')
    else:
        lines.append('timeline: []')

    lines += [
        f'',
        f'# ── PROFILE ──────────────────────────────────────',
        f'bio: "{data.get("bio", "")}"',
        f'statement: "{data.get("statement", "")}"',
        f'',
        f'# ── SOCIAL ───────────────────────────────────────',
        f'# Always use the full URL for every platform.',
        f'linkedin:  "{data.get("linkedin", "")}"',
        f'instagram: "{data.get("instagram", "")}"',
        f'x:         "{data.get("x", "")}"',
        f'substack:  "{data.get("substack", "")}"',
        f'orcid:     "{data.get("orcid", "")}"',
        f'youtube:   "{data.get("youtube", "")}"',
        f'tiktok:    "{data.get("tiktok", "")}"',
    ]

    content = '\n'.join(lines) + '\n'

    if dry_run:
        return content
    else:
        os.makedirs(FELLOWS_DIR, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return content


def verify_headers(csv_headers, required_fields):
    """Check that required columns exist in the CSV."""
    missing = [f for f in required_fields if f not in csv_headers]
    if missing:
        print(f"ERROR: CSV is missing required column(s): {', '.join(missing)}")
        print(f"       Found columns: {', '.join(csv_headers)}")
        print(f"       See README-SCRIPTS.md for the required column names.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Import a CSV to Fellow YAML files.')
    parser.add_argument('--csv', required=True, help='Path to the input CSV file')
    parser.add_argument('--fields', default='',
                        help='Comma-separated list of fields to update (e.g. bio,statement,linkedin). Required unless --full is set.')
    parser.add_argument('--full', action='store_true',
                        help='Full import — create or completely overwrite Fellow files.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without writing any files.')
    args = parser.parse_args()

    if not args.full and not args.fields:
        print("ERROR: You must specify either --fields or --full.")
        print("  --fields bio,statement,linkedin  (update only those fields)")
        print("  --full                           (create or overwrite entire file)")
        sys.exit(1)

    csv_path = args.csv if os.path.isabs(args.csv) else os.path.join(REPO_ROOT, args.csv)
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found: {csv_path}")
        sys.exit(1)

    fields_to_update = [f.strip() for f in args.fields.split(',') if f.strip()] if args.fields else []

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        csv_headers = reader.fieldnames or []

        # Verify headers
        required = ['slug'] + (fields_to_update if not args.full else [])
        verify_headers(csv_headers, required)

        rows = list(reader)

    if not rows:
        print("CSV is empty — nothing to do.")
        sys.exit(0)

    if args.dry_run:
        print("DRY RUN — no files will be written.\n")

    created = []
    updated = []
    skipped = []

    for row in rows:
        slug = row.get('slug', '').strip()
        if not slug:
            skipped.append(f"  Row {rows.index(row)+2}: missing slug — skipped")
            continue

        existing = load_existing(slug)
        is_new = not existing

        if args.full:
            # Full overwrite — use CSV data for everything, existing data as fallback
            merged = {}
            for col in ALL_COLUMNS:
                merged[col] = row.get(col, existing.get(col, '')) or existing.get(col, '') or ''
            merged['slug'] = slug
        else:
            # Partial update — start with existing data, overlay only specified fields
            merged = dict(existing)
            merged['slug'] = slug
            for field in fields_to_update:
                if field in row and row[field].strip():
                    merged[field] = row[field].strip()
                # If cell is blank and field is in --fields, we do NOT overwrite
                # (blank = "not provided", not "intentionally cleared")

        write_fellow(slug, merged, dry_run=args.dry_run)

        if is_new:
            created.append(slug)
        else:
            updated.append(slug)

    # Summary
    print(f"\n{'DRY RUN — ' if args.dry_run else ''}IMPORT COMPLETE")
    print(f"{'─'*40}")
    if created:
        print(f"  Created ({len(created)}): {', '.join(created)}")
    if updated:
        print(f"  Updated ({len(updated)}): {', '.join(updated)}")
    if skipped:
        print(f"  Skipped ({len(skipped)}):")
        for s in skipped:
            print(s)
    if fields_to_update:
        print(f"\n  Fields updated: {', '.join(fields_to_update)}")
    if not args.dry_run and (created or updated):
        print(f"\n  Review the changes, then commit and push to GitHub.")


if __name__ == '__main__':
    main()
