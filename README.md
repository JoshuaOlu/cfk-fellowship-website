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

→ **[README-TECHNICAL.md](./README-TECHNICAL.md)** — how to run the site locally, how Jekyll collections work, folder structure, and deployment.

---

## Running locally

```bash
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000`.

## Deployment

Push to `main` on GitHub. GitHub Pages builds and deploys automatically.
