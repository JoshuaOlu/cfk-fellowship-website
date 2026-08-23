# CFK Fellowship — Technical Reference

This document explains the site's structure and how the pieces connect. For routine content updates, see [README-MAINTENANCE.md](./README-MAINTENANCE.md).

---

## Tech stack

- **Jekyll 4.3** — static site generator
- **GitHub Pages** — hosting and automatic deployment
- **No plugins** — only Jekyll core features are used, keeping the build compatible with GitHub Pages' default environment
- **No JavaScript frameworks** — vanilla JS only, all inline in page files or the base layout

---

## Folder structure

```
fellowship.careforknowledge.org/
│
├── _config.yml              ← Jekyll config. Site-wide URLs and collection settings.
├── Gemfile                  ← Ruby gem dependencies.
│
├── _data/                   ← All content data. Edit these for routine updates.
│   ├── site_status.yml
│   ├── current_cohort.yml
│   ├── cohorts.yml
│   ├── timeline.yml
│   ├── about.yml
│   ├── autumn-2026-fellows.yml   ← Current cohort (not permanent profiles)
│   └── fellows/             ← One .yml per Fellow with a permanent profile
│       └── [slug].yml
│
├── _layouts/
│   ├── base.html            ← Wraps every page (head, nav, footer)
│   └── fellow.html          ← Individual Fellow profile layout
│
├── _includes/
│   ├── nav.html             ← Status-aware navigation and announcement bar
│   ├── footer.html          ← Site footer
│   └── fellow-card.html     ← Reusable Fellow card (used in directory and cohort pages)
│
├── _fellows/                ← Jekyll collection stubs. One .md per Fellow.
│   └── [slug].md            ← Triggers page generation at /fellows/[slug]/
│
├── assets/
│   ├── css/style.css        ← All styles. One file, clearly sectioned.
│   ├── images/
│   │   ├── fellows/         ← Fellow headshots — named [slug].jpg
│   │   └── cohorts/         ← Current cohort photos (lighter treatment)
│   └── downloads/
│       ├── cfk-fellowship-companion.pdf
│       └── reports/         ← Cohort reports — named [season-year].pdf
│
├── index.html               ← Homepage (status-aware template)
├── about/index.html         ← About page
├── fellows/index.html       ← Fellows directory
└── cohorts/
    ├── index.html           ← Cohorts archive
    ├── spring-2025/index.html
    ├── spring-2026/index.html
    └── autumn-2026/index.html
```

---

## How Fellow pages work

Jekyll's **collections** feature generates one HTML page per Fellow automatically.

**The flow:**
1. A stub file exists at `_fellows/israel-oladejo.md` with `layout: fellow` and `fellow_slug: israel-oladejo`
2. Jekyll processes this and renders it using `_layouts/fellow.html`
3. The layout reads `site.data.fellows['israel-oladejo']` to get all the profile data
4. The output is published at `/fellows/israel-oladejo/`

**Why two files per Fellow?**
- `_data/fellows/[slug].yml` holds the data — easy to read and edit in plain YAML
- `_fellows/[slug].md` is the trigger that makes Jekyll generate the page — just 3 lines

This separation keeps data and generation concerns clean. All editing happens in `_data/fellows/`.

**Adding a new Fellow:**
Both files are required. If either is missing, the profile page won't appear.

---

## How the status system works

`_data/site_status.yml` has one field: `status`.

Every template that needs to behave differently reads this:
```liquid
{% assign status = site.data.site_status.status %}
{% if status == "recruiting" %}...{% endif %}
```

The nav (`_includes/nav.html`), homepage (`index.html`), and individual page CTAs all read from the same source. Change the one field and everything updates.

---

## How current cohort Fellows work

Current Foundation Fellows (who don't have permanent profile pages yet) are stored in `_data/autumn-2026-fellows.yml` as a simple list with just `first_name`, `last_name`, `track`, and `photo`.

They appear on:
- The cohort page (`/cohorts/autumn-2026/`) — headshot, name, track
- The Fellows directory — same lighter card treatment

When they graduate, they move out of this list and into `_data/fellows/` with a full profile.

---

## CSS architecture

All styles are in `assets/css/style.css`. The file is sectioned with clear headers:
- Design tokens (`:root` variables)
- Reset and base
- Layout utilities
- Navigation
- Buttons
- Type utilities
- Homepage hero and sections
- Page headers
- About page
- Fellows directory
- Individual Fellow profiles
- Cohort pages
- Footer
- Responsive breakpoints

No CSS preprocessor is used. If adding new page styles, add a clearly labelled section at the bottom.

---

## Running locally

Requirements: Ruby 3+, Bundler

```bash
# Install dependencies (first time only)
bundle install

# Start local server
bundle exec jekyll serve

# Build without serving
bundle exec jekyll build
```

Site is at `http://localhost:4000`. Jekyll watches for file changes and rebuilds automatically.

---

## Deployment

Pushes to `main` on GitHub trigger an automatic build via GitHub Pages. No manual build step required.

Build time is typically under 30 seconds for this site size.

If a build fails, check the Actions tab on GitHub for the error. The most common causes are:
- YAML syntax error in a `_data/` file (indentation, missing quotes, stray colon)
- A missing file referenced in a template (e.g. a fellow_slug that has no matching `_data/fellows/` file)

---

## Adding a new cohort page

1. Create `cohorts/[season-year]/index.html`
2. Copy `cohorts/spring-2026/index.html` as the template
3. Update the `slug` in the `where:` filter to match the new cohort's slug
4. Update the page title and description in the front matter
5. Add the cohort entry to `_data/cohorts.yml`
6. Create `_data/[season-year]-fellows.yml` for the current cohort Foundation Fellows

---

## Design tokens

Colours are defined as CSS variables in `:root` in `style.css`:

```css
--navy:      #060F5B;   /* Primary dark background */
--cyan:      #0BECD6;   /* Primary accent — links, highlights, badges */
--pink:      #FF1BA2;   /* Secondary accent — eyebrows, special badges */
--mint:      #89FEB8;   /* Tertiary accent — Associate Fellow badge */
--white:     #FFFFFF;
--off:       #F7F7F7;   /* Light grey background for sections */
--text:      #1A1A1A;
--muted:     #666;
--border:    #E8E8E8;
```

Change a variable here and it updates everywhere it's used.
