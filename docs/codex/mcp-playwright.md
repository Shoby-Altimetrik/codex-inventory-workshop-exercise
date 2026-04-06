# Codex MCP Primer: Playwright

## Why MCP Matters
Model Context Protocol (MCP) lets Codex use tools beyond local file editing. In this workshop, the most useful example is browser automation so participants can verify interactive behavior instead of relying only on unit tests.

## What To Teach
- MCP extends what Codex can do, not just what it can read.
- Tool access should be intentional and scoped to the task.
- Browser automation is strongest when paired with tests and screenshots.

## Workshop Framing
- Exercises 1-6 focus on repo understanding, specs, and code changes.
- Exercise 7 introduces browser automation as a verification layer.
- Exercise 8 turns that into reviewable visual evidence.

## Example Setup Snippet
Use a placeholder example for discussion:

```toml
# ~/.codex/config.toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]
```

## Participant Prompt
`Use browser automation to open the local app, verify the orders search flow, and save screenshots of the result.`

## Teaching Note
The point of this step is not “use more tools.” It is “choose the right verification surface for the problem.”
