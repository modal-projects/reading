from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import typer
import yaml

app = typer.Typer(help="Agent-native helpers for reading spikes.")
spike_app = typer.Typer(help="Create and refresh spike scaffolds.")
site_app = typer.Typer(help="Validate and build the site.")
app.add_typer(spike_app, name="spike")
app.add_typer(site_app, name="site")

ROOT = Path(__file__).resolve().parent.parent
CONTENT_ROOT = ROOT / "src" / "content" / "spikes"
PUBLIC_ROOT = ROOT / "public" / "spikes"


@dataclass
class SpikePaths:
    slug: str
    content_dir: Path
    page_path: Path
    sources_path: Path
    public_asset_dir: Path


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-")


def spike_paths(slug: str) -> SpikePaths:
    content_dir = CONTENT_ROOT / slug
    return SpikePaths(
      slug=slug,
      content_dir=content_dir,
      page_path=content_dir / "index.mdx",
      sources_path=content_dir / "sources.json",
      public_asset_dir=PUBLIC_ROOT / slug / "assets",
    )


def now_date() -> str:
    return datetime.now(UTC).date().isoformat()


def resolve_signer() -> str | None:
    """Return the current Modal username, or None if it can't be resolved.

    Used by `reading spike create` to prefill `addedBy`. Never raises; callers
    should treat a None result as "leave the field for the agent to fill".
    """
    try:
        result = subprocess.run(
            ["uv", "run", "python", "scripts/modal_identity.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    username = result.stdout.strip()
    return username or None


def default_spike_mdx(title: str, slug: str, added_by: str | None) -> str:
    signer = added_by or "TODO"
    return f"""---
title: "{title}"
summary: "TODO: Replace with a concise overview of the topic."
theme: "TODO: Name the central systems or research theme."
whyItMatters: "TODO: Explain why this topic matters for the team."
tags:
  - TODO
updatedAt: {now_date()}
sourceCount: 0
addedBy: {signer}
---
import SourceList from "../../../components/SourceList.astro";
import sources from "./sources.json";

## Overview

TODO: Frame the topic in plain language. Explain what changed, why it matters, and what the
reader should take away.

## Key themes

- TODO: Theme one
- TODO: Theme two
- TODO: Theme three

## Suggested reading order

1. TODO
2. TODO
3. TODO

<SourceList sources={{sources}} />
"""


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path} is missing frontmatter")
    _, remainder = text.split("---\n", 1)
    frontmatter_text, body = remainder.split("\n---\n", 1)
    data = yaml.safe_load(frontmatter_text) or {}
    return data, body


def write_frontmatter(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    rendered = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    path.write_text(f"---\n{rendered}\n---\n{body}")


def load_sources(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def validate_spike(slug: str) -> list[str]:
    paths = spike_paths(slug)
    errors: list[str] = []

    if not paths.page_path.exists():
      return [f"{slug}: missing page {paths.page_path}"]
    if not paths.sources_path.exists():
      return [f"{slug}: missing sources file {paths.sources_path}"]

    try:
        frontmatter, _ = read_frontmatter(paths.page_path)
    except Exception as exc:  # noqa: BLE001
        return [f"{slug}: failed to parse frontmatter: {exc}"]

    sources = load_sources(paths.sources_path)
    required = ["title", "summary", "theme", "whyItMatters", "tags", "updatedAt", "sourceCount", "addedBy"]
    for key in required:
        if key not in frontmatter:
            errors.append(f"{slug}: missing frontmatter key {key}")

    if str(frontmatter.get("addedBy", "")).strip() in {"", "TODO"}:
        errors.append(f"{slug}: addedBy must be set to a Modal username (run scripts/modal_identity.py)")

    if frontmatter.get("sourceCount") != len(sources):
        errors.append(
            f"{slug}: sourceCount={frontmatter.get('sourceCount')} does not match {len(sources)} source entries"
        )

    for source in sources:
        for field in ["id", "title", "kind", "canonicalUrl", "summary", "whyRelevant", "addedBy"]:
            if field not in source:
                errors.append(f"{slug}: source {source.get('id', '<unknown>')} missing field {field}")
        if str(source.get("addedBy", "")).strip() in {"", "TODO"}:
            errors.append(
                f"{slug}: source {source.get('id', '<unknown>')} addedBy must be set to a Modal username"
            )
        pdf_path = source.get("pdfPath")
        if pdf_path:
            pdf_file = ROOT / "public" / pdf_path.removeprefix("/").removeprefix("public/")
            if not pdf_file.exists():
                errors.append(f"{slug}: missing PDF asset {pdf_path}")

    return errors


@spike_app.command("create")
def create_spike(topic: str) -> None:
    slug = slugify(topic)
    paths = spike_paths(slug)
    paths.content_dir.mkdir(parents=True, exist_ok=True)
    paths.public_asset_dir.mkdir(parents=True, exist_ok=True)

    signer = resolve_signer()
    if not paths.page_path.exists():
        paths.page_path.write_text(default_spike_mdx(topic.title(), slug, signer))
    if not paths.sources_path.exists():
        paths.sources_path.write_text("[]\n")

    if signer:
        typer.echo(f"Scaffolded spike '{slug}' (signed by {signer})")
    else:
        typer.echo(
            f"Scaffolded spike '{slug}' with addedBy: TODO — run scripts/modal_identity.py and fill it in"
        )


@spike_app.command("refresh")
def refresh_spike(slug: str) -> None:
    paths = spike_paths(slug)
    if not paths.page_path.exists():
        raise typer.BadParameter(f"Spike '{slug}' does not exist")

    frontmatter, body = read_frontmatter(paths.page_path)
    sources = load_sources(paths.sources_path)
    frontmatter["updatedAt"] = now_date()
    frontmatter["sourceCount"] = len(sources)
    write_frontmatter(paths.page_path, frontmatter, body)
    typer.echo(f"Refreshed spike '{slug}'")


@site_app.command("validate")
def validate_site() -> None:
    slugs = sorted(path.name for path in CONTENT_ROOT.iterdir() if path.is_dir())
    errors: list[str] = []
    for slug in slugs:
        errors.extend(validate_spike(slug))
    if errors:
        for error in errors:
            typer.echo(error, err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Validated {len(slugs)} spikes")


@site_app.command("build")
def build_site() -> None:
    subprocess.run(["uv", "run", "reading", "site", "validate"], cwd=ROOT, check=True)
    subprocess.run(["npm", "run", "build"], cwd=ROOT, check=True)
