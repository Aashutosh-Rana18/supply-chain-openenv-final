# Submission Checklist

## Environment Logic

- [x] `reset()`, `step()`, and `state()` are implemented.
- [x] Three tasks exist: `easy`, `medium`, and `hard`.
- [x] The grader returns normalized scores in the `0.0` to `1.0` range.
- [x] `inference.py` exists at the repo root.

## Validator-Facing Files

- [x] `uv.lock` exists at the repo root.
- [x] `pyproject.toml` defines both `inference` and `server` in `[project.scripts]`.
- [x] `server/app.py` exists and can run the FastAPI server.
- [x] `openenv.yaml` exists and parses cleanly.
- [x] `Dockerfile` starts the API on port `7860`.

## Local Verification

- [ ] `uv run inference`
- [ ] `uv run server --host 0.0.0.0 --port 7860`
- [ ] `python -m pytest -q`
- [ ] `python scripts/validate_openenv.py`

## Notes

- This checklist is intentionally focused on the OpenEnv validation flow.
- Hugging Face-specific submission steps were removed from the repo docs.
