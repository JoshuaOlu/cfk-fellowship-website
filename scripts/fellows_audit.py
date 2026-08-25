"""
fellows_audit.py
────────────────
Scans all Fellow YAML files and produces a report of what is missing
or needs attention. No files are changed — this is read-only.

Saves a dated log to scripts/logs/audit_YYYY-MM-DD.txt

USAGE
  python scripts/fellows_audit.py
  python scripts/fellows_audit.py --csv       # also export a CSV of issues
"""

import os
import sys
import csv
import argparse
from datetime import date

REPO_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELLOWS_DIR = os.path.join(REPO_ROOT, '_data', 'fellows')
STUBS_DIR   = os.path.join(REPO_ROOT, '_fellows')
LOGS_DIR    = os.path.join(REPO_ROOT, 'scripts', 'logs')

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml")
    sys.exit(1)

SOCIAL_FIELDS = ['linkedin', 'instagram', 'x', 'substack', 'orcid', 'youtube', 'tiktok']


def load_all_fellows():
    """Load all Fellow YAML files. Returns list of (slug, data) tuples."""
    fellows = []
    errors = []
    if not os.path.isdir(FELLOWS_DIR):
        print(f"ERROR: {FELLOWS_DIR} not found.")
        sys.exit(1)

    for fname in sorted(os.listdir(FELLOWS_DIR)):
        if not fname.endswith('.yml'):
            continue
        slug = fname[:-4]
        path = os.path.join(FELLOWS_DIR, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            fellows.append((slug, data))
        except Exception as e:
            errors.append((slug, str(e)))

    return fellows, errors


def audit_fellow(slug, data):
    """Return a dict of issues for one Fellow."""
    issues = []

    # Missing bio
    if not data.get('bio', '').strip():
        issues.append('missing bio')

    # Missing statement
    if not data.get('statement', '').strip():
        issues.append('missing statement')

    # Missing photo
    photo = data.get('photo', '').strip()
    if not photo:
        issues.append('no photo path set')
    else:
        # Check if the actual file exists
        photo_path = os.path.join(REPO_ROOT, photo.lstrip('/'))
        if not os.path.exists(photo_path):
            issues.append(f'photo path set but file not found ({photo})')

    # Missing all social links
    socials = [data.get(s, '').strip() for s in SOCIAL_FIELDS]
    if not any(socials):
        issues.append('no social links')

    # Alumni with no exit date
    if data.get('status') == 'alumni' and not data.get('exited', '').strip():
        issues.append('alumni with no exit date')

    # Emeritus but not Senior/Principal
    if data.get('status') == 'emeritus':
        level = data.get('level', '')
        if level not in ('Senior Fellow', 'Principal Fellow'):
            issues.append(f'emeritus but level is "{level}" (should be Senior or Principal)')

    # Missing stub file
    stub_path = os.path.join(STUBS_DIR, f'{slug}.md')
    if not os.path.exists(stub_path):
        issues.append('missing _fellows stub file (profile page will not generate)')

    # Slug mismatch
    if data.get('slug', '').strip() != slug:
        issues.append(f'slug field "{data.get("slug")}" does not match filename "{slug}"')

    return issues


def format_report(fellows, errors, issues_map):
    """Format the full audit report as a string."""
    lines = []
    today = date.today().strftime('%d %B %Y')

    lines.append('CFK FELLOWSHIP — FELLOWS AUDIT')
    lines.append(f'Generated: {today}')
    lines.append('═' * 60)
    lines.append('')

    # Summary counts
    total        = len(fellows)
    active       = sum(1 for _, d in fellows if d.get('status') == 'active')
    alumni       = sum(1 for _, d in fellows if d.get('status') == 'alumni')
    emeritus     = sum(1 for _, d in fellows if d.get('status') == 'emeritus')
    with_issues  = sum(1 for s, _ in fellows if issues_map.get(s))
    missing_bio  = sum(1 for s, _ in fellows if 'missing bio' in issues_map.get(s, []))
    missing_stmt = sum(1 for s, _ in fellows if 'missing statement' in issues_map.get(s, []))
    no_photo     = sum(1 for s, _ in fellows if any('photo' in i for i in issues_map.get(s, [])))
    no_socials   = sum(1 for s, _ in fellows if 'no social links' in issues_map.get(s, []))

    lines.append('SUMMARY')
    lines.append('─' * 40)
    lines.append(f'  Total Fellows:       {total}')
    lines.append(f'  Active:              {active}')
    lines.append(f'  Alumni:              {alumni}')
    lines.append(f'  Emeritus:            {emeritus}')
    lines.append('')
    lines.append(f'  Fellows with issues: {with_issues} of {total}')
    lines.append(f'  Missing bio:         {missing_bio}')
    lines.append(f'  Missing statement:   {missing_stmt}')
    lines.append(f'  Photo issues:        {no_photo}')
    lines.append(f'  No social links:     {no_socials}')
    if errors:
        lines.append(f'  YAML read errors:    {len(errors)}')
    lines.append('')

    # YAML errors
    if errors:
        lines.append('YAML ERRORS (fix these first)')
        lines.append('─' * 40)
        for slug, err in errors:
            lines.append(f'  {slug}: {err}')
        lines.append('')

    # Fellows with issues
    fellows_with_issues = [(s, d, issues_map[s]) for s, d in fellows if issues_map.get(s)]
    if fellows_with_issues:
        lines.append('FELLOWS WITH ISSUES')
        lines.append('─' * 40)
        for slug, data, issues in fellows_with_issues:
            name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip() or slug
            level = data.get('level', '')
            status = data.get('status', '')
            lines.append(f'  {name} ({slug})')
            lines.append(f'    Level: {level}  |  Status: {status}')
            for issue in issues:
                lines.append(f'    ✗ {issue}')
            lines.append('')
    else:
        lines.append('✅ No issues found — all Fellows look good.')
        lines.append('')

    # Clean Fellows
    clean = [(s, d) for s, d in fellows if not issues_map.get(s)]
    if clean:
        lines.append('FELLOWS WITH NO ISSUES')
        lines.append('─' * 40)
        for slug, data in clean:
            name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
            lines.append(f'  ✓ {name} ({slug})')
        lines.append('')

    lines.append('─' * 60)
    lines.append('End of audit.')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Audit all Fellow profiles for missing data.')
    parser.add_argument('--csv', action='store_true',
                        help='Also export a CSV of Fellows with issues to scripts/logs/')
    args = parser.parse_args()

    fellows, errors = load_all_fellows()
    if not fellows and not errors:
        print("No Fellow YAML files found in _data/fellows/")
        sys.exit(0)

    issues_map = {}
    for slug, data in fellows:
        issues_map[slug] = audit_fellow(slug, data)

    report = format_report(fellows, errors, issues_map)

    # Print to terminal
    print(report)

    # Save log file
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_filename = f"audit_{date.today().strftime('%Y-%m-%d')}.txt"
    log_path = os.path.join(LOGS_DIR, log_filename)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📄 Log saved to: scripts/logs/{log_filename}")

    # Optional CSV export of issues
    if args.csv:
        csv_path = os.path.join(LOGS_DIR, f"audit_{date.today().strftime('%Y-%m-%d')}_issues.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['slug', 'name', 'level', 'status', 'issues'])
            for slug, data in fellows:
                if issues_map.get(slug):
                    name = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
                    writer.writerow([
                        slug, name,
                        data.get('level', ''),
                        data.get('status', ''),
                        '; '.join(issues_map[slug])
                    ])
        print(f"📊 Issues CSV saved to: scripts/logs/{os.path.basename(csv_path)}")


if __name__ == '__main__':
    main()
