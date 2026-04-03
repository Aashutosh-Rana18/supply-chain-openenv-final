# Deployment Guide

This repository is prepared for the OpenEnv validator flow and local FastAPI execution.

## Pre-Submission Checks

Run these commands from the repo root:

```bash
uv lock
uv run inference
uv run server --host 0.0.0.0 --port 7860
python -m pytest -q
python scripts/validate_openenv.py
```

## Required Submission Files

The validator expects these artifacts to be present and consistent:

- `uv.lock`
- `pyproject.toml`
- `openenv.yaml`
- `inference.py`
- `server/app.py`
- `Dockerfile`

## GitHub Submission

Push the repository to GitHub and submit the repository URL used for your OpenEnv project.

## Troubleshooting

- If the validator says `server` is missing, check `[project.scripts]` in `pyproject.toml`.
- If it says `openenv-core` is missing, re-check both `pyproject.toml` and `uv.lock`.
- If local tests pick up the wrong package, confirm imports resolve to this repository rather than an older global install.
