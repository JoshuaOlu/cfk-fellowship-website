# CFK Fellowship Website

The official website for the [CFK Fellowship](https://fellowship.careforknowledge.org) — a Care for Knowledge initiative.

Built with Jekyll and hosted on GitHub Pages.

---

## Quick orientation

This site has five public pages:

| Page | URL | What it is |
|---|---|---|
| Homepage | `/` | Status-aware landing page. Changes based on whether we're recruiting, reviewing, active, or between cohorts. |
| About | `/about/` | What the Fellowship is, the three commitments, and the key timeline of our history. |
| Fellows | `/fellows/` | Directory of all Fellows — active, alumni, and emeritus — grouped by level. |
| Fellow profile | `/fellows/[name]/` | Permanent individual page for each Fellow. |
| Cohorts | `/cohorts/` | Archive linking to each cohort page. |
| Cohort page | `/cohorts/[season-year]/` | Individual cohort page with Fellows and report link. |

**Everything you routinely update lives in `_data/`.** You should almost never need to touch the HTML files.

---

## The `_data/` folder — where you work

```
_data/
├── site_status.yml         ← ONE field. Controls the whole homepage.
├── current_cohort.yml      ← Details of the active or upcoming cohort.
├── cohorts.yml             ← Archive of every cohort.
├── timeline.yml            ← Key dates shown on the About page.
├── about.yml               ← Programme description. Rarely changes.
├── autumn-2026-fellows.yml ← Current cohort Foundation Fellows (no profile pages yet).
└── fellows/                ← One file per Fellow. Add/edit here.
    ├── joshua-olunlade.yml
    ├── israel-oladejo.yml
    └── ...
```

---

## 👉 See the full maintenance guide

→ **[README-MAINTENANCE.md](./README-MAINTENANCE.md)** — step-by-step instructions for every routine task: changing site status, adding Fellows, graduating a cohort, uploading photos, publishing reports.

→ **[README-FELLOWS.md](./README-FELLOWS.md)** — everything about Fellow profiles: the YAML schema, what each field means, how to add social links, what to do when a Fellow graduates, advances, or leaves.

→ **[README-SCRIPTS.md](./README-SCRIPTS.md)** — the automation scripts. Export/import Fellows as CSV, bulk-update profiles, graduate cohorts, and set up new cohorts with a single command.

→ **[README-TECHNICAL.md](./README-TECHNICAL.md)** — how to run the site locally, how Jekyll collections work, folder structure, and deployment.

---

## The data management toolkit

For team members managing Fellow records and cohort data, two tools exist alongside this repo:

**Google Sheets template** (`scripts/templates/CFK_Fellowship_Data_Template.xlsx`)
Upload this to Google Drive and it converts automatically to a Google Sheet. Four sheets:
- **Fellows Directory** — full Fellow records with dropdowns for Level, Status, Track, Cohort
- **Cohort Setup** — enter new Foundation Fellows when starting a new cohort
- **Targeted Updates** — record promotions, alumni markings, role changes
- **Export Guide** — step-by-step instructions for exporting each sheet as CSV

**CSV templates** (`scripts/templates/`)
The raw CSV format the scripts consume. Use these if you're working directly from the command line without the Google Sheet.

---

## Running locally

```bash
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000`.

## Deployment

Push to `main` on GitHub. GitHub Pages builds and deploys automatically.
