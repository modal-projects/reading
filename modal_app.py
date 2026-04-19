from __future__ import annotations

from pathlib import Path

import fastapi
import fastapi.staticfiles
import modal

ROOT = Path(__file__).resolve().parent

app = modal.App("reading-site")

image = (
    modal.Image.from_registry("node:20-bookworm", add_python="3.12")
    .pip_install("fastapi[standard]==0.115.12")
    .add_local_dir(
        ROOT,
        remote_path="/app",
        copy=True,
        ignore=[
            ".astro",
            ".git",
            ".github",
            ".jj",
            ".npm-cache",
            ".venv",
            "dist",
            "node_modules",
            "result",
        ],
    )
    .run_commands("cd /app && npm ci")
    .run_commands("cd /app && npm run build", force_build=True)
)

web_app = fastapi.FastAPI()


@app.function(image=image, scaledown_window=1800)
@modal.concurrent(max_inputs=100)
@modal.asgi_app(label="read")
def serve():
    web_app.mount("/", fastapi.staticfiles.StaticFiles(directory="/app/dist", html=True))
    return web_app
