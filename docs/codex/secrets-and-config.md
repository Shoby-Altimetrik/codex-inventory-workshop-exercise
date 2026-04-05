# Codex Secrets And Config Walkthrough

## Goal
Show how to discuss secrets, config, and external keys safely during a workshop without storing real credentials in the repository.

## Rules
- Never commit real keys.
- Use placeholders in examples.
- Keep environment-specific values out of tracked workshop files.

## Safe Demo Pattern
1. Explain the integration at a conceptual level.
2. Show where a participant would normally configure a key.
3. Use a placeholder like `OPENAI_API_KEY=your-key-here`.
4. Emphasize that real values belong in local environment configuration, not git.

## Example Prompt
`Show me how this project would be configured to use an external API key without committing the secret to the repository. Use placeholders only.`

## Workshop Tie-In
This fits best as an instructor-led sidebar during Exercises 1 or 7 when discussing Codex setup, MCP servers, or future integrations.
