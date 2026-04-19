# Reading

An agent-native reading site. Spikes are short, opinionated notes on systems topics with an annotated reading list. Live at [modal-labs--read.modal.run](https://modal-labs--read.modal.run).

## Setup

You don't edit this site by hand. You point a coding agent (Cursor, Claude Code, Codex, etc.) at the repo and ask it to add a paper or create a spike. Before the agent can write anything Modal-specific, you need two things configured:

1. **A Notion MCP connection** so the agent can read Modal's internal planning docs, roadmap pages, and customer asks. The agent uses this to write `whyItMatters` text that reflects actual Modal priorities instead of generic industry framing. Configure it in your editor by following Notion's guide: [Connecting to Notion MCP](https://developers.notion.com/guides/mcp/get-started-with-mcp). Cursor, Claude Code, Codex, VS Code (Copilot), Windsurf, and more are covered. Without this, the agent will pause and ask you for internal context rather than making something up.
2. **Modal CLI authenticated to the `modal-labs` workspace** if you want the agent to deploy. Confirm with `modal profile current`; activate with `modal profile activate modal-labs` if needed.

Optional but helpful: the repo-local Nix shell (`nix develop`) pins the Node and Python versions, but `uv` and `npm` work directly if your system versions are close enough to `flake.nix` and `.nvmrc`.

## Skills

The repo ships four skills under `.agents/skills/` that an agent will read and follow. When you prompt the agent, name the skill for the step you want — most modern agents will invoke the right one automatically, but being explicit helps.

- **`spike-planner`** — turns a broad topic into a spike brief (title, slug, theme, `whyItMatters`). Searches Modal's Notion first for internal framing.
- **`spike-researcher`** — picks 4–8 sources, mirrors PDFs into `public/spikes/<slug>/assets/`, and writes `sources.json` with `whyRelevant` annotations grounded in Notion context.
- **`spike-generator`** — writes the MDX overview, key themes, and opinionated reading order, then runs `reading spike refresh` to keep metadata honest.
- **`site-steward`** — validates, builds, checks `modal profile current` returns `modal-labs`, and deploys. Refuses to deploy from the wrong workspace.

Every spike and source is signed with the Modal username (e.g. `alessio-modal-labs`) of the person who curated it — the same handle `modal app history` shows. Agents resolve the signer with `uv run python scripts/modal_identity.py` and write it into `addedBy`. The site renders it as "Curated by @username" on spikes and "Added by @username" on each source card.

## Add a paper

### Adding a paper to an existing spike

Open the agent in a checkout of this repo and paste a prompt like:

> Add this paper to the site using the `spike-researcher` skill, then deploy with `site-steward`:
>
> `https://arxiv.org/abs/2604.15039`

The agent will read the existing spikes under `src/content/spikes/`, pick the one where the paper actually fits, search Modal's Notion via MCP for relevant internal context, mirror the PDF into `public/spikes/<slug>/assets/`, add a source entry to `sources.json` (with a Modal-specific `whyRelevant`), update the spike's overview/reading order if the new source shifts the story, and run `uv run reading spike refresh <slug>` to keep `sourceCount` and `updatedAt` honest.

### Creating a new spike

If the paper doesn't fit any existing spike, tell the agent:

> This paper doesn't fit any of our spikes — create a new one.
>
> Use `spike-planner` to frame it (search Notion for the Modal priority this maps onto), then `spike-researcher` for adjacent sources, then `spike-generator` to write the page. Deploy with `site-steward`.
>
> `<paper url>`

The agent will:

1. Plan the spike — title, slug, theme, `whyItMatters` — grounded in whatever Modal Notion context it finds.
2. Scaffold with `uv run reading spike create "<topic>"`.
3. Research adjacent sources (4–8 total is the target).
4. Write the spike page and source summaries.
5. Validate, build, and deploy.

You can help by saying what angle you care about ("focus on systems tradeoffs, not benchmark numbers") and which adjacent work belongs in the reading list. If the Notion MCP server isn't configured or the agent can't find internal context, it will stop and ask rather than making up a `whyItMatters`.

## Running things by hand

If you want to run the tooling directly:

```bash
nix develop          # or make sure uv + node are on PATH
uv sync
npm ci

uv run reading spike create "<topic>"   # scaffold
uv run reading spike refresh <slug>     # bump sourceCount + updatedAt
uv run reading site validate            # check frontmatter, source fields, PDF paths
npm run build                           # local build smoke test
npm run dev                             # local preview at http://localhost:4321

modal profile activate modal-labs       # shared deployment workspace
uv run modal deploy modal_app.py        # publish to modal-labs--read.modal.run
```

## Structure

- `AGENTS.md` — repo operating contract for coding agents.
- `.agents/skills/` — the four skills described above (planner, researcher, generator, site-steward).
- `reading_repo/` — Python tooling for scaffolding and validation.
- `src/` — Astro site (layouts, components, pages, MDX spike content).
- `public/spikes/<slug>/assets/` — mirrored PDFs and other static spike assets.
- `modal_app.py` — the Modal ASGI app that builds the site in an image and serves `dist/`.
