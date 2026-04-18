# Reading

An agent-native reading site for team-relevant spikes.

## Quick start

```bash
nix develop
uv sync
npm install
uv run reading spike create "multi-tenant lora for rl"
npm run dev
```

## Core commands

```bash
uv run reading spike create "<topic>"
uv run reading spike refresh <slug>
uv run reading site validate
npm run build
```

## Deploy

```bash
source ~/.codex/modal.env
nix develop -c uv run modal deploy modal_app.py
```

## Structure

- `AGENTS.md`: repo operating contract for Codex.
- `.agents/skills/`: repo-local skills for planning, research, generation, and site stewardship.
- `reading_repo/`: Python tooling for scaffolding and validation.
- `src/`: Astro site.
- `public/spikes/`: mirrored PDFs and other static spike assets.
