# Architecture

Version: 1.0 (Draft)

## Purpose

This document explains how the CFK Fellowship website is structured and the engineering principles that guide its development.

The objective is to keep the project simple, maintainable, fast, and easy for future contributors to understand.

---

# Technology Stack

## Static Site Generator

Jekyll

Reasons:

- Native support on GitHub Pages
- Markdown-first content authoring
- Excellent SEO
- No database required
- Minimal infrastructure
- Easy for new contributors to learn

---

## Hosting

GitHub Pages

Reasons:

- Free hosting
- Automatic deployment
- Version controlled
- Reliable
- Supports custom domains

---

## Styling

Vanilla CSS

Reasons:

- No framework dependency
- Small bundle size
- Complete design control
- Easier to understand
- Better long-term maintainability

---

## JavaScript

Vanilla JavaScript

JavaScript should only be introduced when necessary.

Examples:

- Mobile navigation
- Theme switching (future)
- Search (future)

Interactive behaviour should progressively enhance the experience rather than be required for it.

---

# Directory Structure

```
/
│
├── _includes/
│
├── _layouts/
│
├── _posts/
│
├── assets/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── icons/
│
├── pages/
│
├── blog/
│
├── DESIGN.md
├── ARCHITECTURE.md
├── DECISIONS.md
│
└── README.md
```

---

# Architectural Principles

## 1. Component Driven

Repeated interface elements belong inside `_includes`.

Examples:

- Navigation
- Footer
- Hero
- CTA
- FAQ
- Timeline

---

## 2. Layout Driven

Every page should inherit from a layout.

Layouts define structure.

Pages define content.

---

## 3. Content Driven

Content should be written in Markdown whenever practical.

Avoid writing HTML unless necessary.

---

## 4. Progressive Enhancement

Every page should remain functional without JavaScript.

JavaScript should enhance—not replace—the user experience.

---

## 5. Mobile First

Layouts are designed for small screens first.

Desktop enhancements are added using media queries.

---

## 6. Accessibility First

Semantic HTML is preferred over generic elements.

Accessibility should never be deferred until the end of development.

---

# CSS Architecture

```
variables.css

↓

base.css

↓

layout.css

↓

components.css

↓

utilities.css
```

## variables.css

Design tokens

- colours
- spacing
- typography
- shadows
- radius

## base.css

Global defaults

## layout.css

Containers

Grid

Sections

Page layouts

## components.css

Buttons

Cards

Navigation

Hero

Timeline

Forms

FAQ

Footer

## utilities.css

Small reusable utility classes.

---

# Images

Images should be:

- optimized
- responsive
- descriptive
- compressed

Decorative images should not contain important information.

---

# SEO

Every page should include:

- unique title
- unique description
- canonical URL
- semantic headings
- descriptive alt text

The project aims for Lighthouse SEO scores of 100.

---

# Performance

Performance is a feature.

Guidelines:

- minimise JavaScript
- optimise images
- minimise CSS
- avoid unnecessary libraries
- lazy load large assets

---

# Deployment

Main branch

↓

GitHub Pages

↓

fellowship.careforknowledge.org

Deployment should remain automatic.

---

# Future Architecture

Potential additions:

- Blog
- Fellowship Handbook
- Resource Library
- Search
- Alumni Profiles
- Cohort Pages

These additions should integrate into the existing architecture rather than require major restructuring.

---

# Guiding Principle

Prefer simplicity over cleverness.

Future contributors should be able to understand the project with minimal onboarding.