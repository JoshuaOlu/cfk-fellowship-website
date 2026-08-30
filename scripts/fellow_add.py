"""
fellow_add.py
─────────────
Add a single new Fellow. Creates both the YAML data file and the
Jekyll collection stub file that generates their profile page.

MODES
  Interactive — run with no arguments, answer questions one by one:
    python scripts/fellow_add.py

  Arguments — pass everything on the command line:
    python scripts/fellow_add.py \\
      --first "Amara" --last "Obi" --track "WikiQuestions" \\
      --cohort "Spring 2027" --level "Foundation Fellow" \\
      --vid "20270001"

  CSV — add one Fellow from a single-row CSV:
    python scripts/fellow_add.py --csv new_fellow.csv

The script checks whether a Fellow with the same slug already exists
and asks for confirmation before overwriting.

WHAT IT CREATES
  _data/fellows/[slug].yml   — the Fellow's data file
  _fellows/[slug].md         — the Jekyll stub that generates their page
"""

import os
import sys
import csv
import argparse
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELLOWS_DIR = os.path.join(REPO_ROOT, '_data', 'fellows')
STUBS_DIR  = os.path.join(REPO_ROOT, '_fellows')

sys.path.insert(0, os.path.dirname(__file__))

def clean_text(value):
    """
    Fix common encoding garbling from Google Sheets CSV exports.
    Google Sheets exports UTF-8 without BOM; if read with wrong encoding,
    special characters appear garbled. This fixes the most common cases.
    """
    if not value:
        return value
    # Try to fix UTF-8 bytes misread as latin-1/cp1252
    try:
        fixed = value.encode('latin-1').decode('utf-8')
        return fixed
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    # Manual fallback for the most common garbled sequences
    replacements = {
        'â€"': '—',   # em dash
        'â€™': "'",   # right single quote
        'â€˜': "'",   # left single quote
        'â€œ': '"',   # left double quote
        'â€':  '"',   # right double quote
        'â€¦': '…',   # ellipsis
        'Ã©':  'é',
        'Ã¨':  'è',
        'Ã ':  'à',
        'Ã¢':  'â',
        'Ã®':  'î',
        'Ã´':  'ô',
        'Ã»':  'û',
        'Ã§':  'ç',
        'Ã«':  'ë',
        'Ã¯':  'ï',
        'Ã¼':  'ü',
        'Ã¶':  'ö',
        'Ã¤':  'ä',
        'Ã±':  'ñ',
    }
    for garbled, correct in replacements.items():
        value = value.replace(garbled, correct)
    return value

def clean_row(row):
    """Apply clean_text to every value in a CSV row dict."""
    return {k: clean_text(v) if isinstance(v, str) else v for k, v in row.items()}

def normalise_headers(reader):
    """
    Strip asterisks and extra whitespace from CSV column headers.
    This allows headers like 'slug *' or 'first_name *' (used in the
    Google Sheets template as visual hints) to be read as 'slug', 'first_name'.
    """
    reader.fieldnames = [
        f.replace('*', '').strip()
        for f in (reader.fieldnames or [])
    ]
    return reader



from fellows_import import write_fellow, load_existing

TRACKS = ['WikiQuestions', 'CTRI', 'Model NASS', 'CFK Fellowship']
LEVELS = ['Foundation Fellow', 'Associate Fellow', 'Senior Fellow', 'Principal Fellow']
STATUSES = ['active', 'alumni', 'emeritus']


def make_slug(first, last):
    """Generate a URL-safe slug from first and last name."""
    name = f"{first}-{last}".lower()
    name = re.sub(r"[^a-z0-9\-]", '-', name)
    name = re.sub(r"-+", '-', name).strip('-')
    return name


def create_stub(slug):
    """Create the Jekyll collection stub file."""
    os.makedirs(STUBS_DIR, exist_ok=True)
    path = os.path.join(STUBS_DIR, f'{slug}.md')
    content = f"---\nlayout: fellow\nfellow_slug: {slug}\n---\n"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def ask(prompt, default='', options=None):
    """Prompt the user for input, with an optional default and option list."""
    if options:
        print(f"  Options: {', '.join(options)}")
    if default:
        display = f"{prompt} [{default}]: "
    else:
        display = f"{prompt}: "
    while True:
        val = input(display).strip()
        if not val and default:
            return default
        if not val:
            print("  (required — please enter a value)")
            continue
        if options and val not in options:
            print(f"  Please choose one of: {', '.join(options)}")
            continue
        return val


def interactive_mode():
    """Collect Fellow details interactively."""
    print("\nCFK Fellowship — Add a New Fellow")
    print("─" * 40)
    print("Press Enter to accept the default value shown in [brackets].\n")

    data = {}
    data['first_name'] = ask("First name")
    data['last_name']  = ask("Last name")

    slug = make_slug(data['first_name'], data['last_name'])
    existing = load_existing(slug)
    if existing:
        print(f"\n  ⚠️  A Fellow with slug '{slug}' already exists.")
        confirm = input("  Overwrite? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("  Aborted.")
            sys.exit(0)

    print(f"  → Slug will be: {slug}")

    data['vid']          = ask("VID (Volunteer ID, e.g. 20270001)", default='')
    data['track']        = ask("Track", options=TRACKS)
    data['cohort']       = ask("Cohort (e.g. Spring 2027)")
    data['level']        = ask("Level", default='Foundation Fellow', options=LEVELS)
    data['status']       = ask("Status", default='active', options=STATUSES)
    data['joined']       = ask("Joined (e.g. Spring 2027)", default=data['cohort'])
    data['exited']       = ask("Exited (leave blank for active Fellows)", default='')
    data['current_role'] = ask("Current role (e.g. WikiQuestions Digitization Fellow)", default='')
    data['photo']        = ask(f"Photo path", default=f"/assets/images/fellows/{slug}.jpg")

    print("\n  Social links — paste the full URL or leave blank.")
    for platform in ('linkedin', 'instagram', 'x', 'substack', 'orcid', 'youtube', 'tiktok'):
        data[platform] = ask(f"  {platform}", default='')

    data['bio']          = ask("Bio (2-4 sentences, or leave blank for now)", default='')
    data['statement']    = ask("Statement (optional, leave blank for now)", default='')

    # Empty list fields
    data['other_roles'] = ''
    data['timeline']    = ''
    data['profile_visible'] = False  # Default hidden; update once consent is given

    return slug, data


def csv_mode(csv_path):
    """Load Fellow details from a single-row CSV."""
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        normalise_headers(reader)
        rows = [clean_row(r) for r in reader]

    if not rows:
        print("ERROR: CSV is empty.")
        sys.exit(1)
    if len(rows) > 1:
        print(f"WARNING: CSV has {len(rows)} rows. Only the first row will be used.")
        print("To add multiple Fellows, use fellows_import.py --full instead.")

    row = rows[0]
    first = row.get('first_name', '').strip()
    last  = row.get('last_name', '').strip()
    if not first or not last:
        print("ERROR: CSV must have 'first_name' and 'last_name' columns.")
        sys.exit(1)

    slug = row.get('slug', '').strip() or make_slug(first, last)
    return slug, row


def args_mode(args):
    """Build Fellow data from command-line arguments."""
    first = args.first
    last  = args.last
    slug  = args.slug or make_slug(first, last)
    data = {
        'first_name':   first,
        'last_name':    last,
        'vid':          args.vid or '',
        'track':        args.track or '',
        'cohort':       args.cohort or '',
        'level':        args.level or 'Foundation Fellow',
        'status':       'active',
        'joined':       args.cohort or '',
        'exited':       '',
        'current_role': '',
        'photo':        f"/assets/images/fellows/{slug}.jpg",
        'other_roles':  '',
        'timeline':     '',
        'bio':          '',
        'statement':    '',
        'linkedin': '', 'instagram': '', 'x': '',
        'substack': '', 'orcid': '', 'youtube': '', 'tiktok': '',
        'profile_visible': False,  # New fellows default to hidden until consent given
    }
    return slug, data


def main():
    parser = argparse.ArgumentParser(description='Add a single new Fellow.')
    parser.add_argument('--first',  help='First name')
    parser.add_argument('--last',   help='Last name')
    parser.add_argument('--slug',   help='Override the auto-generated slug')
    parser.add_argument('--vid',    help='Volunteer ID')
    parser.add_argument('--track',  help='Track', choices=TRACKS)
    parser.add_argument('--cohort', help='Cohort name (e.g. "Spring 2027")')
    parser.add_argument('--level',  help='Level', choices=LEVELS, default='Foundation Fellow')
    parser.add_argument('--csv',    help='Path to a single-row CSV file')
    args = parser.parse_args()

    # Determine mode
    if args.csv:
        csv_path = args.csv if os.path.isabs(args.csv) else os.path.join(REPO_ROOT, args.csv)
        if not os.path.exists(csv_path):
            print(f"ERROR: CSV not found: {csv_path}")
            sys.exit(1)
        slug, data = csv_mode(csv_path)
    elif args.first and args.last:
        slug, data = args_mode(args)
    else:
        slug, data = interactive_mode()

    # Check for existing Fellow
    existing = load_existing(slug)
    if existing and not args.csv:
        # Interactive already checked; for args/csv mode, confirm here
        print(f"\n⚠️  Fellow '{slug}' already exists.")
        confirm = input("Overwrite? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Aborted.")
            sys.exit(0)

    # Write YAML
    yaml_path = os.path.join(FELLOWS_DIR, f'{slug}.yml')
    write_fellow(slug, data)

    # Write stub
    stub_path = create_stub(slug)

    print(f"\n✅ Fellow added successfully!")
    print(f"   YAML:  _data/fellows/{slug}.yml")
    print(f"   Stub:  _fellows/{slug}.md")
    print(f"   Page will be at: /fellows/{slug}/")
    print(f"\nNEXT STEPS:")
    print(f"  → Upload headshot to: assets/images/fellows/{slug}.jpg")
    print(f"  → Add bio and statement to: _data/fellows/{slug}.yml")
    print(f"  → Commit and push to GitHub.")


if __name__ == '__main__':
    main()
