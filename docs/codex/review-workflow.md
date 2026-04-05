# Review Workflow

## Default workshop-authoring flow
1. Branch from `main`.
2. Keep changes grouped by theme.
3. Validate the baseline and changed docs locally.
4. Open a review PR before merging.

## Recommended branch model
- `main`: canonical intentionally failing workshop baseline
- review branch: workshop-authoring work for Shoby review
- participant branches: solution or demo work during exercises

## What to summarize for reviewers
- what changed
- what remains intentionally broken
- what new Codex teaching was added
- what is deferred to later phases

## Advanced option
Use worktrees when you want to prototype workshop ideas in isolation without disturbing the main authoring branch.
