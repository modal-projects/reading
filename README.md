# Reading

An agent-native reading site. Spikes are short, opinionated notes on systems topics with an annotated reading list. Live at [modal-labs--reading.modal.run](https://modal-labs--reading.modal.run).

## Add a paper

You don't edit this site by hand. You point a coding agent (Cursor, Codex, Claude Code, etc.) at the repo and ask it to add a paper. The agent reads `AGENTS.md` and the skills under `.agents/skills/` and takes it from there.

### Adding a paper to an existing spike

Open the agent in a checkout of this repo and paste a prompt like:

> Add this paper to the site and deploy: `https://arxiv.org/abs/2604.15039`

The agent will read the existing spikes under `src/content/spikes/`, pick the one where the paper actually fits, mirror the PDF into `public/spikes/<slug>/assets/`, add a source entry to `sources.json` (with a real `summary` and `whyRelevant`), update the spike's overview/reading order if the new source shifts the story, and run `uv run reading spike refresh <slug>` to keep `sourceCount` and `updatedAt` honest.

### Creating a new spike

If a paper doesn't fit any existing spike, just tell the agent:

> This paper doesn't fit any of our existing spikes — create a new one around it.
>
> `<paper url>`

The agent will:

1. Plan the spike (title, slug, theme, why it matters) using the `spike-planner` skill.
2. Scaffold it with `uv run reading spike create "<topic>"`.
3. Research adjacent sources (4–8 total is the target) using the `spike-researcher` skill.
4. Write the spike page and source summaries using the `spike-generator` skill.

You can help it a lot by saying what angle you care about ("focus on the systems tradeoffs, not the benchmark numbers") and which adjacent work belongs in the reading list. The agent will ask if it needs clarification.

### Deploying

After content changes, ask the agent to deploy. The `site-steward` skill validates, builds, checks that `modal profile current` returns `modal-labs`, and then runs `modal deploy modal_app.py`. If the Modal profile is anything other than `modal-labs`, the agent will stop and ask you to switch rather than fork a parallel deployment at a different URL.

## Running things by hand

If you want to run the tooling directly:

```bash
nix develop          # or just make sure uv + node are on PATH
uv sync
npm ci

uv run reading spike create "<topic>"   # scaffold
uv run reading spike refresh <slug>     # bump sourceCount + updatedAt
uv run reading site validate            # check frontmatter, source fields, PDF paths
npm run build                           # local build smoke test
npm run dev                             # local preview server

modal profile activate modal-labs       # make sure you're on the shared workspace
uv run modal deploy modal_app.py        # publish to modal-labs--reading.modal.run
```

## Structure

- `AGENTS.md` — repo operating contract for coding agents.
- `.agents/skills/` — repo-local skills for planning, researching, generating, and deploying spikes.
- `reading_repo/` — Python tooling for scaffolding and validation.
- `src/` — Astro site (layouts, components, pages, MDX spike content).
- `public/spikes/<slug>/assets/` — mirrored PDFs and other static spike assets.
- `modal_app.py` — the Modal ASGI app that builds the site in an image and serves `dist/`.
