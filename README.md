# AI-Augmented Git Workflow Assistant

A privacy-friendly CLI that reads a real Git diff and generates useful commit messages, pull-request summaries, and structured change metadata. The deterministic generator works offline; its validation layer is designed to guard future LLM output against claims that are not grounded in the diff.

## Why it matters

Commit messages and PR descriptions are often written in a hurry. Generic AI summarizers can also invent behavior that the code does not contain. This project starts from the source of truth—the diff—and keeps file paths and change counts visible in every summary.

## Install and use

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"

git-assist inspect
git-assist commit --staged
git-assist pr --staged
pytest
```

## Safety design

- Reads only `git diff`; it never commits, pushes, or modifies source files.
- Parses per-file additions, deletions, creations, and removals.
- Generates a useful offline fallback with no API key.
- Exposes a validator that compares generated terminology with paths and changed lines.
- Fails visibly when unsupported terminology is detected instead of silently returning a misleading summary.

## Architecture

`Git diff -> parser -> structured change model -> generator -> grounding validator -> terminal output`

The provider boundary can be extended with an LLM call while keeping the same validator and offline fallback. Secrets should be supplied through environment variables, never committed to the repository.
