# CFK Fellowship — Maintenance Guide

This guide covers every routine task you will need to do to keep the site up to date. You do not need to understand how Jekyll works to follow these steps.

---

## Changing what the homepage shows

The homepage has four modes. You switch between them by editing one line in `_data/site_status.yml`:

```yaml
status: "recruiting"
```

Change the value to one of these four options:

| Value | When to use |
|---|---|
| `recruiting` | Applications are open. Homepage shows the apply CTA. |
| `reviewing` | Applications closed, we are selecting Fellows. Homepage says "selections in progress." |
| `active` | The cohort is running. Homepage says "now active" and links to the Fellows page. |
| `between` | Nothing is happening. Homepage shows the evergreen version with a waitlist form. |

That single change also updates the announcement bar and the nav button automatically.

---

## Opening a new cohort for applications

When you are ready to recruit for a new cohort:

**Step 1 — Update `_data/current_cohort.yml`:**
- Set `name`, `season`, `year`, `slug` for the new cohort
- Set `start_month`, `end_month`, `full_date_range`
- Set `apply_url` to the new Google Form application link
- Update the `recruiting.announcement` message text

**Step 2 — Update `_data/site_status.yml`:**
```yaml
status: "recruiting"
```

**Step 3 — Add the new cohort to `_data/cohorts.yml`** at the top of the list:
```yaml
- name: "Spring 2027"
  slug: "spring-2027"
  season: "Spring"
  year: "2027"
  date_range: "February – May 2027"
  fellow_count: 0       # update this when selections are made
  status: "active"
  founding: false
  description: "A short description of this cohort."
  report_url: ""
```

**Step 4 — Create the cohort page folder and file:**
- Create a new folder: `cohorts/spring-2027/`
- Copy `cohorts/autumn-2026/index.html` into that folder
- Open the copied file and update these two lines near the top:

```
title: "Autumn 2026 Cohort"
```
Change to:
```
title: "Spring 2027 Cohort"
```

And:
```
{% assign cohort_data = site.data.cohorts | where: "slug", "autumn-2026" | first %}
{% assign fellows = site.data.autumn-2026-fellows %}
```
Change to:
```
{% assign cohort_data = site.data.cohorts | where: "slug", "spring-2027" | first %}
{% assign fellows = site.data.spring-2027-fellows %}
```

Those are the only lines you need to touch in that file.

---

## When applications close

```yaml
# _data/site_status.yml
status: "reviewing"
```

No other changes needed. The announcement bar and nav button update automatically.

---

## When the cohort begins (Fellows selected)

**Step 1 — Create `_data/[cohort-slug]-fellows.yml`** (e.g. `spring-2027-fellows.yml`):
Copy `_data/autumn-2026-fellows.yml` as a template and fill in the new Foundation Fellows' names and tracks.

**Step 2 — Update the cohort page** to reference the new data file.
Open `cohorts/spring-2027/index.html` and find this line near the top:
```
{% assign fellows = site.data.autumn-2026-fellows %}
```
Change `autumn-2026-fellows` to match your new data file name — e.g. `spring-2027-fellows`.

**Step 3 — Update `_data/cohorts.yml`:** set `fellow_count` to the actual number selected.

**Step 4 — Change status:**
```yaml
status: "active"
```

---

## When a cohort ends (graduating Fellows)

When a cohort finishes, Foundation Fellows who completed it get permanent profile pages.

For each graduating Fellow:

**Step 1 — Create their Fellow YAML file** in `_data/fellows/`. See [README-FELLOWS.md](./README-FELLOWS.md) for the full template and field guide.

**Step 2 — Create their collection stub file** in `_fellows/`. Copy any existing `.md` file in `_fellows/`, rename it to `[firstname-lastname].md`, and update the `fellow_slug` line:
```yaml
---
layout: fellow
fellow_slug: firstname-lastname
---
```

**Step 3 — Remove them from the cohort Fellows list** (the `_data/[cohort]-fellows.yml` file).

**Step 4 — Update `_data/cohorts.yml`:** change the cohort's `status` from `"active"` to `"completed"`, and add the report URL when it's ready:
```yaml
status: "completed"
report_url: "/assets/downloads/reports/autumn-2026.pdf"
```

**Step 5 — Upload the cohort report PDF** to `assets/downloads/reports/`.

---

## Publishing a cohort report

1. Save the PDF as `assets/downloads/reports/[season-year].pdf`
   Example: `assets/downloads/reports/autumn-2026.pdf`

2. Add the path to `_data/cohorts.yml` for the relevant cohort:
   ```yaml
   report_url: "/assets/downloads/reports/autumn-2026.pdf"
   ```

A "Read Cohort Report" button appears automatically on the cohort page and the cohorts index.

---

## Updating a Fellow's details

Open their file in `_data/fellows/` and edit the relevant fields. For example, if someone advances to Associate Fellow:
```yaml
level: "Associate Fellow"   # was "Foundation Fellow"
```

Save the file and push to GitHub. The site updates automatically.

---

## When a Fellow leaves

1. Open `_data/fellows/[slug].yml`
2. Change `status` from `"active"` to `"alumni"`
3. Set `exited` to the month and year they left (e.g. `"December 2026"`)
4. Push to GitHub

Their profile page stays live at the same URL. They move to the collapsible Alumni section of the Fellows directory. The profile header changes colour and a notice is added automatically — no extra work needed.

**If they reached Senior or Principal Fellow level,** use `"emeritus"` instead of `"alumni"`. This gives them the Emeritus card (dark navy, pink accent) and moves them to the Emeritus section, which is always visible above the Alumni section. See [README-FELLOWS.md](./README-FELLOWS.md) for the full Emeritus process.

---

## Adding a cohort to the key timeline

The timeline on the About page is curated — only milestone moments, not every cohort. Edit `_data/timeline.yml` and add an entry:

```yaml
- date: "Spring 2027"
  label: "A short milestone label"
  description: "One or two sentences about why this moment matters."
```

Add entries at the bottom of the list (they appear in the order listed, oldest first).

---

## Updating the site-wide links

Edit `_config.yml` for:
- `cfk_url` — the main CFK website
- `companion_url` — path to the Fellowship Companion PDF
- `email` — fellowship contact email
- `instagram_url`, `twitter_url`, `linkedin_url`

---

## If something looks broken

1. Check that you didn't accidentally delete a `---` line at the top or bottom of a YAML file. Every YAML file must have exactly the structure shown in the examples.
2. Check that indentation uses spaces, not tabs.
3. If a Fellow's page isn't appearing, make sure their slug in `_data/fellows/[slug].yml` matches the filename exactly, and that a corresponding `.md` file exists in `_fellows/`.
4. Run `bundle exec jekyll serve` locally to see error messages in the terminal.
