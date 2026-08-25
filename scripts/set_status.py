"""
set_status.py
─────────────
Change the site status with a single command.
Updates _data/site_status.yml and prints what the announcement bar will say.

USAGE
  python scripts/set_status.py recruiting
  python scripts/set_status.py reviewing
  python scripts/set_status.py active
  python scripts/set_status.py between

STATUS VALUES
  recruiting  Applications open. Homepage shows full apply CTA.
  reviewing   Applications closed, selections in progress.
  active      Cohort is running. No recruitment.
  between     Between cohorts, nothing imminent.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_FILE  = os.path.join(REPO_ROOT, '_data', 'site_status.yml')
COHORT_FILE  = os.path.join(REPO_ROOT, '_data', 'current_cohort.yml')

VALID_STATUSES = ['recruiting', 'reviewing', 'active', 'between']

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml")
    sys.exit(1)


def get_announcement(status, cohort):
    """Return what the announcement bar will say for each status."""
    name = cohort.get('name', '[cohort name]') if cohort else '[cohort name]'
    messages = {
        'recruiting': f"Applications for the {name} Cohort are now open.",
        'reviewing':  f"Applications for the {name} Cohort are now closed. We are reviewing applications.",
        'active':     cohort.get('active', {}).get('announcement', f"The {name} Cohort is underway.") if cohort else f"The {name} Cohort is underway.",
        'between':    "No cohort is currently running. The next cohort will be announced in due course.",
    }
    return messages.get(status, '')


def main():
    if len(sys.argv) < 2:
        print("USAGE: python scripts/set_status.py [status]")
        print(f"       Valid values: {', '.join(VALID_STATUSES)}")
        sys.exit(1)

    new_status = sys.argv[1].strip().lower()

    if new_status not in VALID_STATUSES:
        print(f"ERROR: '{new_status}' is not a valid status.")
        print(f"       Valid values: {', '.join(VALID_STATUSES)}")
        sys.exit(1)

    # Read current status
    current_status = None
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        current_status = data.get('status')

    if current_status == new_status:
        print(f"Status is already '{new_status}' — no change made.")
        sys.exit(0)

    # Load cohort info for announcement preview
    cohort = None
    if os.path.exists(COHORT_FILE):
        with open(COHORT_FILE, 'r', encoding='utf-8') as f:
            cohort = yaml.safe_load(f)

    # Write new status
    content = f"# Updated by set_status.py\nstatus: \"{new_status}\"\n"
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    announcement = get_announcement(new_status, cohort)

    print(f"\n✅ Site status changed: '{current_status}' → '{new_status}'")
    print(f"\n   Announcement bar will read:")
    print(f"   \"{announcement}\"")
    print(f"\n   Nav CTA button: ", end='')
    cta = {'recruiting': 'Apply Now', 'reviewing': 'Join Waitlist',
           'active': 'Join Waitlist', 'between': 'Express Interest'}
    print(cta.get(new_status, ''))
    print(f"\n   Commit and push to GitHub to go live.")


if __name__ == '__main__':
    main()
