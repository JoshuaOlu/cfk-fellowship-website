# CFK Fellowship — Automation Scripts

These scripts automate the most repetitive tasks in managing the Fellowship website. They run locally on your computer — you run one command, the files in your repo update, then you review and push to GitHub.

---

## Before you start — one-time setup

All scripts require **PyYAML**. Install it once:

```
pip install pyyaml
```

Confirm it worked:
```
python -c "import yaml; print('ready')"
```

All commands are run from the **root of the repo folder** (the same folder that contains `_config.yml`).

---

## Quick reference

| Script | What it does | When to use it |
|---|---|---|
| `fellows_export.py` | All Fellow YAMLs → one CSV | To review all Fellows, share with the team, or prepare a bulk edit |
| `fellows_import.py` | CSV → Fellow YAML files | After collecting bios/socials from a form; bulk updates |
| `fellows_update.py` | Update specific fields for specific Fellows | Promoting a Fellow, marking alumni, single targeted changes |
| `fellow_add.py` | Add one new Fellow | After a cohort graduates — add each Fellow individually |
| `fellows_audit.py` | Check what's missing across all profiles | Before publishing, after a cohort graduates |
| `cohort_graduate.py` | Graduate Fellows from a cohort | When a cohort ends — creates permanent pages |
| `cohort_new.py` | Set up a new cohort from scratch | When starting a new recruitment cycle |
| `set_status.py` | Change the site status | Whenever the site phase changes |

---

## The standard CSV format

Every script that reads or writes a CSV uses these column headers:

```
slug, vid, first_name, last_name, photo, status, level, track,
cohort, joined, exited, current_role, other_roles, timeline,
bio, statement, linkedin, instagram, x, substack, orcid, youtube, tiktok
```

**List fields** (`other_roles`, `timeline`) use semicolons to separate multiple values within a single cell:
```
other_roles:  "RMC Team Lead; Model NASS Steering Committee"
timeline:     "CTRI Math Team Lead (Feb 2025 – present); RMC Lead (Mar 2025 – present)"
```

**Social links** — always the full URL:
```
linkedin:   https://linkedin.com/in/username
instagram:  https://instagram.com/username
x:          https://x.com/username
substack:   https://username.substack.com
orcid:      https://orcid.org/0000-0000-0000-0000
youtube:    https://youtube.com/@username
tiktok:     https://tiktok.com/@username
```

---

## fellows_export.py

Reads every file in `_data/fellows/` and writes a single CSV with one row per Fellow.

**Usage:**
```bash
python scripts/fellows_export.py
```

**Output:** `scripts/fellows_export.csv`

**Options:**
```bash
# Custom output path
python scripts/fellows_export.py --output my_folder/fellows.csv
```

**When to use:**
- To get a full picture of the Fellowship in a spreadsheet
- To prepare a CSV for bulk editing (edit the CSV, then re-import with `fellows_import.py`)
- To share Fellow data with the team

Fellows are sorted alphabetically by last name in the output.

---

## fellows_import.py

Takes a CSV and creates or updates Fellow YAML files. The `--fields` flag is the safety mechanism — only the columns you name are written. Blank cells in the CSV do **not** overwrite existing data unless the field is in `--fields`.

**Usage:**
```bash
# Update only bio, statement, and social links for existing Fellows
python scripts/fellows_import.py --csv collected_details.csv --fields bio,statement,linkedin,instagram,x,substack,orcid,youtube,tiktok

# Full import — create or completely overwrite Fellow files
python scripts/fellows_import.py --csv new_fellows.csv --full

# Preview changes without writing anything
python scripts/fellows_import.py --csv collected_details.csv --fields bio,statement --dry-run
```

**Required CSV columns:**
- `slug` — always required (identifies which Fellow to update)
- Plus any columns you pass to `--fields`

**The script verifies your column headers first.** If a required column is missing, it tells you exactly what is wrong before doing anything.

**Workflow — using with Google Form responses:**

1. Peace exports the Google Form responses as a CSV
2. Make sure the form question labels match the column names above (e.g. the bio question is labelled "bio", the LinkedIn question is labelled "linkedin")
3. Run:
   ```bash
   python scripts/fellows_import.py --csv form_responses.csv --fields bio,statement,linkedin,instagram,x,substack,orcid,youtube,tiktok
   ```
4. Review what changed, commit and push

---

## fellows_update.py

Update specific fields for one or many Fellows. Only the fields you name are touched — everything else is left exactly as it is.

**Usage — single Fellow:**
```bash
# Promote a Fellow to Senior
python scripts/fellows_update.py --slug israel-oladejo --set level="Senior Fellow"

# Mark as alumni with exit date
python scripts/fellows_update.py --slug grace-chukwuma --set status=alumni --set exited="December 2026"

# Mark as emeritus
python scripts/fellows_update.py --slug joshua-olunlade --set status=emeritus

# Update current role
python scripts/fellows_update.py --slug peace-oyegbola --set current_role="CFK Operations Lead"

# Preview without writing
python scripts/fellows_update.py --slug israel-oladejo --set level="Senior Fellow" --dry-run
```

**Usage — multiple Fellows from a CSV:**

Create a CSV with a `slug` column and the fields you want to update:
```
slug, level
israel-oladejo, Senior Fellow
cornelius-aboderin, Senior Fellow
peace-oyegbola, Associate Fellow
```

Then run:
```bash
python scripts/fellows_update.py --csv promotions.csv --fields level
```

**Notes:**
- Blank cells in the CSV are ignored — they do not overwrite existing data
- The `--set` flag can be repeated for multiple fields in single-Fellow mode
- Always use `--dry-run` first if you are unsure

---

## fellow_add.py

Add a single new Fellow. Creates both the YAML data file and the Jekyll stub file that generates their profile page.

**Mode 1 — Interactive (recommended for most cases):**

Run with no arguments and answer the questions one by one:
```bash
python scripts/fellow_add.py
```

The script will ask for:
- First and last name (auto-generates the slug)
- VID (Volunteer ID)
- Track, cohort, level, status
- Current role
- Photo path (defaults to the standard path)
- Social links
- Bio and statement (you can leave these blank and add later)

**Mode 2 — Arguments:**
```bash
python scripts/fellow_add.py \
  --first "Amara" --last "Obi" \
  --track "WikiQuestions" \
  --cohort "Spring 2027" \
  --level "Foundation Fellow" \
  --vid "20270001"
```

**Mode 3 — CSV:**
```bash
python scripts/fellow_add.py --csv single_fellow.csv
```

The CSV should have the standard column headers. Only the first row is used — for multiple Fellows, use `fellows_import.py --full` instead.

**What it creates:**
- `_data/fellows/[slug].yml`
- `_fellows/[slug].md`

**After running:**
- Upload their headshot to `assets/images/fellows/[slug].jpg`
- Add their bio and statement when they send them
- Commit and push

---

## fellows_audit.py

Scans all Fellow YAML files and reports what is missing or needs attention. No files are changed.

**Usage:**
```bash
python scripts/fellows_audit.py

# Also export a CSV of issues
python scripts/fellows_audit.py --csv
```

**What it checks:**
- Missing bio
- Missing statement
- Missing photo path, or photo path set but file not found
- No social links at all
- Alumni Fellows with no exit date set
- Emeritus Fellows who are not at Senior or Principal level
- Missing Jekyll stub file (profile page would not generate)
- Slug mismatch between filename and YAML content

**Output:**
- Prints a full report to the terminal
- Saves a dated log to `scripts/logs/audit_YYYY-MM-DD.txt`
- With `--csv`: also saves `scripts/logs/audit_YYYY-MM-DD_issues.csv`

**When to run:**
- After a cohort graduates (to see what's missing from new profiles)
- After collecting bios/photos from a form (to confirm everything imported correctly)
- Before a site update (to catch any issues before they go live)

---

## cohort_graduate.py

Graduates Fellows from a cohort. For each Fellow in the graduating CSV:
1. Creates their permanent `_data/fellows/[slug].yml`
2. Creates their `_fellows/[slug].md` stub file
3. Updates the cohort Fellows list to show **only graduates** (non-graduates are removed)

**Usage:**
```bash
python scripts/cohort_graduate.py --cohort autumn-2026 --csv graduating.csv

# Dry run first
python scripts/cohort_graduate.py --cohort autumn-2026 --csv graduating.csv --dry-run
```

**The `--cohort` argument** must match the cohort slug exactly — the same slug used in the filename `_data/autumn-2026-fellows.yml`. So for that file, use `--cohort autumn-2026`.

**Graduating CSV format:**
```
first_name, last_name, track
Amara, Obi, WikiQuestions
Chidi, Eze, CTRI
```

Optional columns: `vid`, `current_role`, `photo`, `slug` (to override auto-generated slug)

**What happens to non-graduates:**
They are removed from the cohort Fellows list file. No YAML or stub file is created for them. They will not appear anywhere on the live site.

**After running:**
1. Run `python scripts/fellows_audit.py` to see what's missing from new profiles
2. Upload headshots to `assets/images/fellows/`
3. Send Fellows the bio/statement collection form
4. Commit and push

---

## cohort_new.py

Sets up everything for a new cohort in one command. This is the script to run when you are about to open applications for the next cohort.

**Usage:**
```bash
python scripts/cohort_new.py \
  --name "Spring 2027" \
  --season spring \
  --year 2027 \
  --fellows new_fellows.csv

# Dry run first
python scripts/cohort_new.py --name "Spring 2027" --season spring --year 2027 \
  --fellows new_fellows.csv --dry-run
```

**Season values:** `spring` or `autumn`
- Spring → date range: February – May
- Autumn → date range: August – November

**Fellows CSV format:**
```
first_name, last_name, track
Amara, Obi, WikiQuestions
Chidi, Eze, CTRI
```

Optional column: `photo` (defaults to standard path)

**What it does automatically:**
- Creates `_data/spring-2027-fellows.yml`
- Creates `cohorts/spring-2027/index.html`
- Adds entry to `_data/cohorts.yml` (at the top — makes it the most recent)
- Rewrites `_data/current_cohort.yml` with the new cohort details
- Sets `_data/site_status.yml` to `recruiting`

**What you still need to do manually (the script tells you):**
- Add the registration form URL to `_data/current_cohort.yml` (`apply_url`)
- Add the waitlist form URL (`waitlist_url`)
- Update the cohort description in `_data/cohorts.yml`
- Upload cohort photos to `assets/images/cohorts/spring-2027/`
- Commit and push

---

## set_status.py

Change the site status with one command. Updates `_data/site_status.yml` and prints a preview of what the announcement bar and nav button will say.

**Usage:**
```bash
python scripts/set_status.py recruiting
python scripts/set_status.py reviewing
python scripts/set_status.py active
python scripts/set_status.py between
```

**When to use each status:**

| Status | When |
|---|---|
| `recruiting` | Applications just opened |
| `reviewing` | Applications closed, selecting Fellows |
| `active` | Cohort has begun |
| `between` | Cohort ended, next one not yet announced |

**Example output:**
```
✅ Site status changed: 'reviewing' → 'active'

   Announcement bar will read:
   "The Spring 2027 Cohort is underway."

   Nav CTA button: Join Waitlist

   Commit and push to GitHub to go live.
```

---

## Typical workflows

### Starting a new cohort from scratch

```bash
# 1. Run the setup script
python scripts/cohort_new.py --name "Spring 2027" --season spring --year 2027 --fellows spring-2027-fellows.csv

# 2. Manually update apply_url and waitlist_url in _data/current_cohort.yml

# 3. Commit and push
```

### After the cohort ends — graduating Fellows

```bash
# 1. Graduate the Fellows
python scripts/cohort_graduate.py --cohort spring-2027 --csv graduates.csv

# 2. Check what's missing
python scripts/fellows_audit.py

# 3. Change status
python scripts/set_status.py between

# 4. Commit and push
```

### Bulk-updating bios after collecting from a form

```bash
# 1. Export current state (optional — for reference)
python scripts/fellows_export.py

# 2. Import the form responses
python scripts/fellows_import.py --csv form_responses.csv --fields bio,statement,linkedin,instagram,x,substack,orcid,youtube,tiktok

# 3. Check what's still missing
python scripts/fellows_audit.py

# 4. Commit and push
```

### Promoting several Fellows to a new level

Create a CSV:
```
slug, level
israel-oladejo, Senior Fellow
cornelius-aboderin, Senior Fellow
```

Then:
```bash
python scripts/fellows_update.py --csv promotions.csv --fields level
```

---

## Troubleshooting

**"PyYAML is not installed"**
Run: `pip install pyyaml`

**"CSV missing required column"**
Check your column header names against the standard list at the top of this document. Headers are case-sensitive.

**"No YAML file found for [slug]"**
The slug you passed doesn't match any file in `_data/fellows/`. Check the slug matches the filename exactly (e.g. `israel-oladejo` matches `_data/fellows/israel-oladejo.yml`).

**"Cohort file not found"**
The `--cohort` argument must match the filename exactly. If the file is `_data/autumn-2026-fellows.yml`, use `--cohort autumn-2026`.

**Changes not appearing on the site**
Make sure you committed and pushed to GitHub after running the script. GitHub Pages rebuilds the site automatically on every push.

**Always use `--dry-run` first** when running a script for the first time or when you are unsure. It shows you exactly what would change without writing anything.
