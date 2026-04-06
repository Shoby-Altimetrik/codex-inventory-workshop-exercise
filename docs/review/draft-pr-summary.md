# Draft PR Summary

## What Changed
- Hardened the workshop baseline so verification fails only where the exercises intend.
- Added Codex-native teaching assets and repo guidance without removing the inventory exercise backbone.
- Reframed the workshop flow so Exercises 1-8 form the core path around setup, context, planning, implementation, verification, and review.

## Intentionally Still Broken
- `main` remains the canonical intentionally failing workshop baseline.
- Bug Fix A remains seeded on baseline.
- Bug Fix B remains seeded on baseline.
- Bug Fix C remains seeded on baseline.
- Feature A remains seeded on baseline.
- Feature B remains seeded on baseline.

## Codex-Native Additions
- `AGENTS.md`
- tracked artifact templates under `output/`
- sample skill scaffold under `.codex/skills/`
- MCP and secrets/config walkthrough docs
- review-branch and reviewer handoff guidance

## How To Review Locally
1. Check out `codex/workshop-codex-alignment`.
2. Run `python3 scripts/validate_guide_sync.py`.
3. Run `./scripts/verify_workshop_state.sh --mode baseline`.
4. Review the live app at `http://localhost:3000`.
5. Review the workshop guide at `http://localhost:4173/workshop-exercises.html`.

## Deferred / Optional
- Exercises 9-10 remain visible but are optional follow-on work for this delivery phase.
- deeper GitHub automation
- broader advanced workflow coverage
- any post-review expansion beyond the current core path
