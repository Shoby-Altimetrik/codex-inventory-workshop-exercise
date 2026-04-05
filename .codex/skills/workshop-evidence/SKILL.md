---
name: "workshop-evidence"
description: "Use when working in this repository to collect a lightweight evidence package after an exercise: summarize the change, point to the relevant tests, and save any requested artifacts under output/."
---

# Workshop Evidence

Use this skill after completing an exercise in the Codex inventory workshop.

## Goal
Produce a small, repeatable evidence bundle that another reviewer can inspect quickly.

## Save Locations
- Specs: `output/spec.md`
- RCA notes: `output/incident-rca.md`
- Architecture notes: `output/architecture-overview.md`
- Screenshots: `output/screenshots/`

## Workflow
1. Identify which exercise was just completed.
2. List the files changed and the smallest relevant test commands.
3. Save or update the expected artifact for that exercise.
4. If browser or visual validation was requested, save screenshots under `output/screenshots/`.
5. End with a concise verification summary.

## Exercise Mapping
- Exercise 1: update `output/architecture-overview.md`
- Exercise 3: update `output/incident-rca.md`
- Exercises 5-6: update `output/spec.md`
- Exercises 7-8: save screenshots and note the validation flow

## Guardrails
- Do not invent passing results.
- Do not overwrite unrelated artifacts.
- Keep evidence short and reviewer-friendly.
