"""
fellows_update.py
─────────────────
Update specific fields for one or many Fellows.
Only the fields you name are changed — everything else is untouched.

USAGE
  # Update one Fellow's level
  python scripts/fellows_update.py --slug israel-oladejo --set level="Senior Fellow"

  # Mark a Fellow as alumni with an exit date
  python scripts/fellows_update.py --slug grace-chukwuma --set status=alumni --set exited="December 2026"

  # Mark a Fellow as emeritus
  python scripts/fellows_update.py --slug joshua-olunlade --set status=emeritus

  # Update multiple Fellows from a CSV (must have 'slug' column + the fields you want)
  python scripts/fellows_update.py --csv promotions.csv --fields level

  # Dry run — preview without writing
  python scripts/fellows_update.py --slug israel-oladejo --set level="Senior Fellow" --dry-run

CSV MODE
  The CSV must have a 'slug' column.
  Use --fields to specify which columns to read from the CSV.
  Blank cells are ignored (they do not overwrite existing data).
"""

import os
import sys
import csv
import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELLOWS_DIR = os.path.join(REPO_ROOT, '_data', 'fellows')

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml")
    sys.exit(1)

# Import the writer from fellows_import
sys.path.insert(0, os.path.dirname(__file__))
from fellows_import import load_existing, write_fellow


def apply_updates(slug, updates, dry_run=False):
    """Load a Fellow's YAML, apply updates, write back."""
    existing = load_existing(slug)
    if not existing:
        print(f"  WARNING: No YAML file found for '{slug}' — skipping.")
        return False

    changed = {}
    for field, value in updates.items():
        old = existing.get(field, '')
        if str(old) != str(value):
            changed[field] = (old, value)
        existing[field] = value

    if not changed:
        print(f"  {slug}: no changes (values already match).")
        return False

    if dry_run:
        print(f"  {slug} (DRY RUN — would change):")
        for field, (old, new) in changed.items():
            print(f"    {field}: '{old}' → '{new}'")
    else:
        write_fellow(slug, existing)
        print(f"  ✅ {slug} updated:")
        for field, (old, new) in changed.items():
            print(f"     {field}: '{old}' → '{new}'")

    return True


def main():
    parser = argparse.ArgumentParser(description='Update specific fields for one or many Fellows.')
    parser.add_argument('--slug', help='Slug of a single Fellow to update')
    parser.add_argument('--set', action='append', metavar='field=value',
                        help='Field to set (e.g. --set level="Senior Fellow"). Repeatable.')
    parser.add_argument('--csv', help='CSV file with slug column and fields to update')
    parser.add_argument('--fields', help='Comma-separated fields to read from CSV')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without writing.')
    args = parser.parse_args()

    if not args.slug and not args.csv:
        print("ERROR: Provide either --slug or --csv.")
        parser.print_help()
        sys.exit(1)

    if args.dry_run:
        print("DRY RUN — no files will be written.\n")

    # ── SINGLE FELLOW MODE ──────────────────────────────────────────────────
    if args.slug:
        if not args.set:
            print("ERROR: --slug requires at least one --set field=value.")
            sys.exit(1)

        updates = {}
        for item in args.set:
            if '=' not in item:
                print(f"ERROR: --set value '{item}' is not in field=value format.")
                sys.exit(1)
            field, _, value = item.partition('=')
            updates[field.strip()] = value.strip().strip('"\'')

        print(f"Updating {args.slug}...")
        apply_updates(args.slug, updates, dry_run=args.dry_run)

    # ── CSV MODE ─────────────────────────────────────────────────────────────
    elif args.csv:
        if not args.fields:
            print("ERROR: --csv requires --fields to specify which columns to update.")
            sys.exit(1)

        csv_path = args.csv if os.path.isabs(args.csv) else os.path.join(REPO_ROOT, args.csv)
        if not os.path.exists(csv_path):
            print(f"ERROR: CSV not found: {csv_path}")
            sys.exit(1)

        fields = [f.strip() for f in args.fields.split(',') if f.strip()]

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []

            if 'slug' not in headers:
                print("ERROR: CSV must have a 'slug' column.")
                sys.exit(1)

            missing = [fd for fd in fields if fd not in headers]
            if missing:
                print(f"ERROR: CSV is missing columns: {', '.join(missing)}")
                sys.exit(1)

            rows = list(reader)

        updated_count = 0
        for row in rows:
            slug = row.get('slug', '').strip()
            if not slug:
                continue
            updates = {}
            for field in fields:
                val = row.get(field, '').strip()
                if val:  # Only update if cell is not blank
                    updates[field] = val
            if updates:
                if apply_updates(slug, updates, dry_run=args.dry_run):
                    updated_count += 1

        print(f"\n{'─'*40}")
        print(f"  {'Would update' if args.dry_run else 'Updated'}: {updated_count} Fellow(s)")
        if not args.dry_run and updated_count:
            print("  Review changes, then commit and push to GitHub.")


if __name__ == '__main__':
    main()
