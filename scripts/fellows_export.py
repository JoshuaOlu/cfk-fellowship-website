"""
fellows_export.py
─────────────────
Reads all Fellow YAML files from _data/fellows/ and writes a single
CSV file with one row per Fellow and every field as a column.

USAGE
  python scripts/fellows_export.py
  python scripts/fellows_export.py --output my_export.csv

OUTPUT
  scripts/fellows_export.csv  (default)

The CSV uses the standard CFK Fellows column format. List fields
(other_roles, timeline) are joined with semicolons within a single cell.
"""

import os
import sys
import csv
import argparse
from datetime import date

# ── Make sure we run from the repo root ──────────────────────────────────────
REPO_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELLOWS_DIR  = os.path.join(REPO_ROOT, '_data', 'fellows')
SCRIPTS_DIR  = os.path.join(REPO_ROOT, 'scripts')
EXPORTS_DIR  = os.path.join(SCRIPTS_DIR, 'exports')

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed.")
    print("Run:  pip install pyyaml")
    sys.exit(1)


# Standard column order — matches the import format
COLUMNS = [
    'slug', 'vid', 'first_name', 'last_name', 'photo',
    'status', 'level', 'track', 'cohort', 'joined', 'exited',
    'current_role', 'other_roles', 'timeline',
    'bio', 'statement',
    'linkedin', 'instagram', 'x', 'substack', 'orcid', 'youtube', 'tiktok',
]


def load_fellow(path):
    """Load a single Fellow YAML file and return as a flat dict."""
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not data:
        return None

    # Flatten list fields to semicolon-separated strings
    for field in ('other_roles', 'timeline'):
        val = data.get(field)
        if isinstance(val, list):
            data[field] = '; '.join(str(v) for v in val if v)
        elif val is None:
            data[field] = ''

    # Ensure all expected columns exist
    for col in COLUMNS:
        if col not in data:
            data[col] = ''
        if data[col] is None:
            data[col] = ''

    return data


def main():
    parser = argparse.ArgumentParser(description='Export all Fellow YAMLs to CSV.')
    today = date.today().strftime('%Y-%m-%d')
    default_output = os.path.join(EXPORTS_DIR, f'fellows_export_{today}.csv')
    parser.add_argument('--output', default=default_output,
                        help=f'Output CSV path (default: scripts/exports/fellows_export_YYYY-MM-DD.csv)')
    args = parser.parse_args()

    if not os.path.isdir(FELLOWS_DIR):
        print(f"ERROR: Fellows directory not found: {FELLOWS_DIR}")
        print("Make sure you are running this from the repo root, or that _data/fellows/ exists.")
        sys.exit(1)

    yml_files = sorted([f for f in os.listdir(FELLOWS_DIR) if f.endswith('.yml')])
    if not yml_files:
        print("No Fellow YAML files found in _data/fellows/")
        sys.exit(0)

    fellows = []
    errors = []

    for filename in yml_files:
        path = os.path.join(FELLOWS_DIR, filename)
        try:
            data = load_fellow(path)
            if data:
                fellows.append(data)
        except Exception as e:
            errors.append(f"  {filename}: {e}")

    if errors:
        print("WARNINGS — could not read these files:")
        for e in errors:
            print(e)
        print()

    # Sort by last name then first name
    fellows.sort(key=lambda f: (f.get('last_name', ''), f.get('first_name', '')))

    # Write CSV — ensure exports/ folder exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', newline='', encoding='utf-8-sig') as f:  # BOM ensures Excel/Sheets reads em dashes and special chars correctly
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(fellows)

    print(f"✅ Exported {len(fellows)} Fellow(s) to: {args.output}")
    if errors:
        print(f"   {len(errors)} file(s) skipped due to errors (see above).")


if __name__ == '__main__':
    main()
