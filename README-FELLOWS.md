# CFK Fellowship — Fellows Guide

Everything about Fellow profiles: how to add them, what each field means, and how to handle every stage of a Fellow's journey.

---

## The Fellow profile system

Every Fellow who has completed their Foundation Cohort gets a permanent profile page at:
```
/fellows/firstname-lastname/
```

This URL **never changes**, even if their level, role, or name changes. It is the permanent link they can put on their CV.

Two files are needed for each Fellow's profile to work:

1. **`_data/fellows/[slug].yml`** — all the Fellow's data (name, level, roles, bio, social links)
2. **`_fellows/[slug].md`** — a short stub file that tells Jekyll to generate the page

Both files must use exactly the same slug (the `firstname-lastname` part).

---

## Adding a new Fellow (after they graduate their Foundation Cohort)

### Step 1 — Choose the slug

The slug is the URL-safe version of their name: lowercase, hyphens instead of spaces.
- Amara Obi → `amara-obi`
- Israel Aponjolosun → `israel-aponjolosun`
- Oluwafunmilade Adewale → `oluwafunmilade-adewale`

If two Fellows share a name exactly, add a number: `israel-oladejo` and `israel-oladejo-2`.

**The slug is set once and never changed.** Even if the person changes their name.

### Step 2 — Create `_data/fellows/[slug].yml`

Copy the template below, fill in every field, and save as `_data/fellows/[slug].yml`:

```yaml
# ── IDENTITY ─────────────────────────────────────────────────
vid: "20270001"         # Volunteer ID from the masterlist
slug: "amara-obi"       # Must match the filename exactly. Never change this.
first_name: "Amara"
last_name: "Obi"
photo: "/assets/images/fellows/amara-obi.jpg"
                        # Leave as "" if no photo yet.

# ── FELLOWSHIP STATUS ─────────────────────────────────────────
status: "active"        # active | alumni | emeritus
level: "Foundation Fellow"
                        # Foundation Fellow | Associate Fellow | Senior Fellow | Principal Fellow
track: "WikiQuestions"  # WikiQuestions | CTRI | Model NASS | CFK Fellowship
cohort: "Spring 2027"   # The cohort this Fellow graduated from
joined: "Spring 2027"   # When they joined. Can be a phrase: "Contributing since 2023; Fellow since Spring 2025"
exited: ""              # Leave blank for active Fellows. For alumni: "December 2027"

# ── CONTRIBUTION RECORD ───────────────────────────────────────
current_role: "WikiQuestions Digitization Fellow"
              # For alumni: their role at the time they left.

other_roles:  # Other roles they currently hold alongside their main role.
  - "RMC Social Media Support"
  # Leave as an empty list if none: other_roles: []

timeline:     # A human-readable record of their roles with dates.
              # Write these in plain language — there's no special format.
  - "WikiQuestions Digitization Fellow (Feb 2027 – present)"
  - "RMC Social Media Support (Mar 2027 – present)"

# ── PROFILE ───────────────────────────────────────────────────
# Fellows write their own bio and statement.
# If they haven't written it yet, leave both as "".
# The section simply won't appear on the page until it's filled.

bio: ""
# 2–4 sentences. Who they are, what they work on, what drives them.
# Plain language, their own voice.

statement: ""
# Optional. One paragraph. Why did you join the Fellowship?
# What are you building? What does this community mean to you?

# ── SOCIAL LINKS ──────────────────────────────────────────────
# Always use the full URL for every platform.
# Leave blank ("") to hide that platform. Hidden fields show no icon.

linkedin:  ""   # https://linkedin.com/in/username
instagram: ""   # https://instagram.com/username
x:         ""   # https://x.com/username
substack:  ""   # https://username.substack.com
orcid:     ""   # https://orcid.org/0000-0000-0000-0000
youtube:   ""   # https://youtube.com/@username
tiktok:    ""   # https://tiktok.com/@username
```

### Step 3 — Create `_fellows/[slug].md`

Create a file at `_fellows/amara-obi.md` with this exact content (just update the slug):

```
---
layout: fellow
fellow_slug: amara-obi
---
```

That's it. Jekyll generates the full profile page from the YAML file automatically.

### Step 4 — Add the headshot

Save the photo at `assets/images/fellows/[slug].jpg` (or `.png`).

Recommended: square crop, minimum 300×300px. The photo displays in a circle.

**If there's no photo yet:** you have two options:
- Leave `photo: ""` — initials show automatically
- Set the path anyway (`photo: "/assets/images/fellows/amara-obi.jpg"`) even before the file exists — initials still show, and the photo appears the moment you upload the file. This is useful if you want to set up the YAML completely and add the photo later.

Either way, the initials fallback is automatic. No broken images will appear.

---

## Field reference — every field explained

| Field | Required? | Notes |
|---|---|---|
| `vid` | Yes | Volunteer ID from the masterlist. Internal only — not shown on the site. |
| `slug` | Yes | Set once, never change. Must match the filename exactly. |
| `first_name` | Yes | First name as displayed. |
| `last_name` | Yes | Last name as displayed. |
| `photo` | No | Path to image. Leave blank for initials placeholder. |
| `status` | Yes | `active`, `alumni`, or `emeritus`. |
| `level` | Yes | Current level (or level at exit for alumni). |
| `track` | Yes | Which CFK programme they contribute to. |
| `cohort` | Yes | The cohort they graduated from. |
| `joined` | Yes | When they joined. Free text — write it naturally. |
| `exited` | Alumni only | Month and year they left (e.g. "December 2026"). Leave blank for active Fellows. The site automatically combines this with the cohort start month to display a date range on the profile: "Fellowship: February 2025 – December 2026". |
| `current_role` | Yes | Their primary role. For alumni: role at time of exit. |
| `other_roles` | No | List of additional current roles. Empty list `[]` if none. |
| `timeline` | No | Human-readable record of roles with dates. |
| `bio` | No | Fellow writes this. 2–4 sentences. Hidden until filled. |
| `statement` | No | Fellow writes this. Optional personal statement. Hidden until filled. |
| `linkedin` through `tiktok` | No | Full URLs for any platform the Fellow wants shown. Leave blank ("") to hide. Always use the complete https:// URL — never just a handle or username. |

---

## When a Fellow advances to the next level

Open their file in `_data/fellows/[slug].yml` and update the `level` field:

```yaml
level: "Associate Fellow"   # was "Foundation Fellow"
```

Update their `timeline` if you want to record when they advanced:
```yaml
timeline:
  - "WikiQuestions Team Lead (Feb 2027 – present)"
  - "Advanced to Associate Fellow: October 2027"
```

---

## When a Fellow leaves

1. Open `_data/fellows/[slug].yml`
2. Change `status` to `"alumni"`
3. Set `exited` to the month and year they left — e.g. `"December 2027"`

```yaml
status: "alumni"
exited: "December 2027"
```

Their profile page stays live at the same permanent URL. They move to the Alumni section of the Fellows directory, which is collapsible by default.

**What changes automatically on their profile page:**
- The header becomes a quieter dark colour (no longer full navy)
- A notice appears: "Their profile remains here as a permanent record of their time with the Fellowship"
- The meta row changes from "Joined" to a date range: "Fellowship: February 2025 – December 2027" — the start month is derived from the cohort name (Spring → February, Autumn → August), so no extra work is needed

---

## Making someone an Emeritus Fellow

Emeritus status is for Fellows who reached **Senior or Principal Fellow level** and made a meaningful extended contribution before stepping back. The title is permanent.

1. Open `_data/fellows/[slug].yml`
2. Change `status` to `"emeritus"`
3. Set `exited` to the month and year they stepped back
4. Confirm `level` shows their correct final level (Senior or Principal Fellow)

```yaml
status: "emeritus"
level: "Senior Fellow"     # or "Principal Fellow"
exited: "December 2027"
```

**What changes automatically:**
- Their card on the Fellows directory moves to the Emeritus section (above Alumni), with a dark navy background and pink accent
- Their profile header stays navy but gains a pink bottom border
- A notice appears on their profile: "Emeritus Fellow. [Name] served as a [Level] and made an extended contribution to CFK's mission before stepping back. The Emeritus title is permanent."
- The date range shows on their profile the same way as Alumni

The Alumni section on the Fellows directory remains collapsible (it does not include Emeritus Fellows — they have their own always-visible section).

---

## Getting bios and statements from Fellows

When a Fellow joins (at graduation), send them a brief:

> **Bio (2–4 sentences):** Who are you? What are you working on in the Fellowship? What drives you?
>
> **Statement (optional, 1 paragraph):** Why did you join the CFK Fellowship? What does being part of this community mean to you?

When they send it, paste it into the `bio` and `statement` fields in their YAML file. No reformatting needed — the site renders it as written.

---

## Collecting social handles from Fellows

You can ask Fellows to share any handles they want listed on their profile page. A simple form or message works:

> Share the full profile URL for any of the following you'd like on your Fellow profile:
> LinkedIn · Instagram · X/Twitter · Substack · ORCID · YouTube · TikTok

Ask them to copy and paste the URL directly from their browser — not just the username. For example: `https://linkedin.com/in/theirname`, not just `theirname`. Only the ones they share will appear. Any blank field is simply invisible on the page.
