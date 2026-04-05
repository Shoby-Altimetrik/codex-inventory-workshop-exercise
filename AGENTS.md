---
name: codex-inventory-workshop
description: Shared project guidance for Codex participants working through the inventory workshop.
---

# Codex Inventory Workshop Instructions

## Purpose
This repository is a teaching project for OpenAI Codex. The goal is not only to fix bugs and ship features, but to demonstrate strong Codex workflows:

- establish repo context before editing
- plan before implementing non-trivial work
- keep diffs tight
- verify with tests, browser checks, and artifacts
- package work on a review branch before merging

## Repository Shape
- `client/`: Vue 3 frontend and Vitest tests
- `server/`: FastAPI backend backed by JSON seed data
- `tests/backend/`: backend regression and feature tests
- `docs/incidents/`: incident packet inputs for response exercises
- `workshop-exercises.html`: static facilitator/participant guide
- `README.md`: full workshop playbook

## Workshop Baseline Rules
- `main` is the canonical intentionally failing baseline.
- Some tests are expected to fail on purpose until participants complete the exercises.
- Do not “clean up” seeded bugs or TODO features unless the active exercise explicitly asks for that change.
- Keep README and `workshop-exercises.html` aligned whenever exercise wording changes.

## Working Style
- Start by summarizing the relevant files and data flow.
- For bug fixes, prefer the smallest safe patch over refactors.
- For feature work, write or approve a short spec first.
- Preserve existing contracts unless the exercise is specifically about changing them.
- If you create artifacts, save them under `output/`.

## Verification Expectations
- Re-run the smallest relevant test set first, then broader checks.
- Use browser validation when the exercise changes interactive behavior.
- Capture evidence when the exercise asks for it:
  - `output/architecture-overview.md`
  - `output/spec.md`
  - `output/incident-rca.md`
  - `output/screenshots/`

## Review Branch Guidance
- Prefer a review branch such as `codex/workshop-codex-alignment`.
- Keep baseline hardening separate from pedagogy/content edits when possible.
- Before review, summarize:
  - what remains intentionally broken
  - what was hardened for workshop delivery
  - what Codex-native teaching was added

## Prompting Reminders
- Ask for architecture or contract traces before patching.
- Ask for a plan when work spans multiple files or layers.
- Ask for a verification checklist at the end of each substantial task.

## Safety Notes
- Do not commit real credentials.
- Use placeholder values for secrets/MCP demos.
- Treat browser automation and screenshots as evidence artifacts, not as a replacement for tests.
