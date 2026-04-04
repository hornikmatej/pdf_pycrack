## Repo Focus

- `src/pdf_pycrack/`: application code
- `tests/`: automated test suite
- `docs/` + `mkdocs.yml`: documentation source and site config
- `benchmark/`: performance tooling and regression checks
- `scripts/`: local maintenance helpers

## Tooling Rules

- Python support starts at 3.12.
- Dependency management is handled with `uv`, and dependency changes must update `uv.lock` in the same change because CI uses frozen syncs.
- `dev` and `docs` are optional extras in `pyproject.toml`, not `uv` dependency groups.
- Add dependencies with:
  - Runtime: `uv add <package>`
  - Dev tooling: `uv add --optional dev <package>`
  - Docs tooling: `uv add --optional docs <package>`

## Common Commands

- Install runtime deps: `uv sync`
- Install dev toolchain: `uv sync --extra dev`
- Install full contributor env: `uv sync --all-extras`
- Run the CLI: `uv run pdf-pycrack <path_to_pdf> [options]`
- Run tests: `uv run pytest`
- Run hooks: `uv run pre-commit run --all-files`
- Build docs: `uv run mkdocs build --strict`
- Run the standard benchmark: `uv run python benchmark/benchmark.py --standard`

## Dependency Refresh Workflow

1. Inspect outdated packages with `uv tree --all-groups --outdated --depth 1`.
2. Update direct requirements with `uv add ...` or `uv add --optional ...`.
3. Refresh locked versions with `uv lock --upgrade`.
4. Sync the environment with `uv sync --all-extras`.
5. Re-run `uv run pytest`, `uv run mkdocs build --strict`, and `uv run pre-commit run --all-files`.
6. Refresh hook revisions with `uv run pre-commit autoupdate` when tooling versions change.

## Documentation Notes

- The API reference pages under `docs/api/` intentionally keep `show_source: false`.
- If you change mkdocstrings versions or re-enable source rendering, verify with `uv run mkdocs build --strict` before merging.

## Commits

- Use Conventional Commits: `feat|fix|chore|docs|test|refactor|build|ci|style|perf|update`
- Prefer `./scripts/committer.sh "type(scope): summary" <paths...>`
- Do not pass `.` to the helper.
