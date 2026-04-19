# Deploy checklist

Run through this in order before and after `uv run modal deploy modal_app.py`.

## Before deploy

- `uv.lock` exists and matches `pyproject.toml`
- `package-lock.json` exists and matches `package.json`
- `uv run reading site validate` passes with no errors
- `npm run build` passes locally
- `uv run modal profile current` returns **exactly** `modal-labs`
  - If not: stop, tell the user, and ask them to run `modal profile activate modal-labs` (or confirm a different target workspace). Deploying from another workspace forks a new deployment at a different URL instead of updating the shared site.

## After deploy

- `modal deploy` exit code is 0
- The printed URL is `https://modal-labs--reading.modal.run`
- The dashboard link (`https://modal.com/apps/modal-labs/main/deployed/reading-site`) shows the new revision with a recent timestamp
