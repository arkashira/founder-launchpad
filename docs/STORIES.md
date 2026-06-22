# STORIES.md

## Overview
This document captures the product backlog for **founder-launchpad**.  
Stories are grouped into **Epics**, ordered by priority to deliver a Minimum Viable Product (MVP) first, then incremental enhancements.  
Each story follows the *As a <role>, I want <goal>, so that <benefit>* format and includes concrete **Acceptance Criteria**.

---

## Epics

| Epic ID | Title | Description |
|---------|-------|-------------|
| **E1** | **Core Scaffold & CLI** | Provide the fundamental “launch a project in 5 minutes” experience: CLI scaffolding, sandbox runner, and basic config handling. |
| **E2** | **Developer Experience & Quality** | Ensure the generated projects are test‑ready, linted, and CI‑integrated out of the box. |
| **E3** | **Extensibility & Plugins** | Enable founders to plug‑in custom data sources, commands, or deployment targets with minimal friction. |
| **E4** | **Telemetry & Usage Insights** | Collect anonymous usage data to guide future improvements while respecting privacy. |
| **E5** | **Documentation & Community Enablement** | Deliver polished docs, examples, and contribution guides to accelerate adoption. |

---

## MVP Stories (E1 → E2)

### E1 – Core Scaffold & CLI

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E1‑S1** | **As a solo founder, I want to generate a new project skeleton with a single command, so that I can start coding immediately.** | - `fl launch my‑app` creates a directory `my‑app/` with a functional Python package.<br>- Scaffold includes `pyproject.toml`, `src/`, `tests/`, and a starter `main.py` that prints “Hello, Founder!”.<br>- Files are populated with the correct package name and entry‑point in `pyproject.toml`.<br>- Command runs in < 2 seconds on a fresh environment. |
| **E1‑S2** | **As a founder, I want the generated project to include a sandbox runner, so that I can execute my code in an isolated environment.** | - `fl sandbox run` creates a temporary virtual environment, installs the project in editable mode, and runs `python -m my_app`.<br>- Sandbox logs are captured and displayed with timestamps.<br>- Runner exits with the same exit code as the executed script. |
| **E1‑S3** | **As a founder, I want a unified configuration manager, so that I can store settings in `.env`, YAML, or JSON without writing boilerplate.** | - Generated project contains `config/` with `settings.yaml` and a `Config` class.<br>- `Config` loads values from environment variables, then YAML, then JSON (priority order).<br>- Invalid schema raises a clear `ConfigError` with line/field details.<br>- Example usage in `main.py` demonstrates retrieving a config value. |
| **E1‑S4** | **As a founder, I want the CLI to display help and version information, so that I can discover commands quickly.** | - `fl --help` lists all top‑level commands with short descriptions.<br>- `fl --version` prints the current toolkit version matching `pyproject.toml`. |
| **E1‑S5** | **As a CI system, I need a default GitHub Actions workflow, so that projects are linted, tested, and packaged automatically.** | - `fl init-ci` adds `.github/workflows/ci.yml` to the scaffold.<br>- Workflow runs on `ubuntu‑latest`, installs Python 3.11, runs `ruff`, `pytest --cov`, and builds a wheel.<br>- Workflow badge appears in the generated README. |

### E2 – Developer Experience & Quality

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E2‑S1** | **As a developer, I want pre‑configured pytest fixtures, so that I can write tests without setup overhead.** | - Scaffold includes `tests/conftest.py` with a `tmp_path` fixture that creates an isolated project copy.<br>- Example test `tests/test_main.py` passes out‑of‑the‑box.<br>- Running `pytest` yields ≥ 95 % coverage on the generated starter code. |
| **E2‑S2** | **As a founder, I want linting rules enforced by default, so that my code stays clean.** | - `ruff` configuration is added to `pyproject.toml` with the “flake8‑compatible” rule set.<br>- `fl lint` command runs `ruff src/ tests/` and exits with non‑zero status on violations.<br>- CI workflow fails on lint errors. |
| **E2‑S3** | **As a maintainer, I need type‑checking integrated, so that type errors are caught early.** | - `mypy` is added to dev dependencies.<br>- `fl type-check` runs `mypy src/` and reports any issues.<br>- CI workflow includes a `type-check` job that must pass. |
| **E2‑S4** | **As a founder, I want a one‑click release command, so that I can publish a wheel to PyPI without manual steps.** | - `fl release` builds a wheel, creates a Git tag, and runs `twine upload` (requires `TWINE_USERNAME`/`TWINE_PASSWORD`).<br>- Command prints a summary URL of the uploaded package.<br>- Failure at any step aborts the release and rolls back the tag. |

---

## Post‑MVP Stories (E3 → E5)

### E3 – Extensibility & Plugins

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E3‑S1** | **As a founder, I want to add custom CLI commands via entry‑points, so that I can extend the toolkit without modifying core code.** | - Documentation shows adding `my_plugin = my_pkg:cli` under `[project.entry-points."founder_launchpad.commands"]` in `pyproject.toml`.<br>- `fl list-plugins` lists discovered commands.<br>- Loaded plugin command executes correctly within the sandbox. |
| **E3‑S2** | **As a data‑driven founder, I want a plugin to pull data from a public API, so that I can prototype data‑centric products quickly.** | - Sample plugin `fl-plugin‑openweather` provided in `examples/`.<br>- Plugin registers `fl fetch-weather --city <name>` and writes JSON to `data/`.<br>- Unit test verifies successful API call (mocked). |
| **E3‑S3** | **As a DevOps engineer, I want the sandbox runner to support Docker back‑ends, so that I can test containerized deployments.** | - `fl sandbox --docker` creates a Docker image with the project, runs it, streams logs.<br>- Runner cleans up containers/images after execution.<br>- Fallback to virtualenv when Docker is unavailable. |

### E4 – Telemetry & Usage Insights

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E4‑S1** | **As a product manager, I want anonymous usage metrics sent on each CLI invocation, so that we can understand feature adoption.** | - Telemetry payload includes command name, OS, Python version, and a UUID stored in `~/.founder_launchpad/telemetry_id`.<br>- Opt‑out flag `fl --no-telemetry` disables sending.<br>- Payload sent over HTTPS to `https://telemetry.axentx.io/collect`. |
| **E4‑S2** | **As a founder, I want to view a local telemetry summary, so that I can see which commands I use most.** | - `fl telemetry report` reads the local log file and prints a table of command counts and timestamps.<br>- Report respects the opt‑out setting. |

### E5 – Documentation & Community Enablement

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E5‑S1** | **As a new user, I want a quick‑start guide in the README, so that I can get a prototype running in < 5 minutes.** | - README includes a “Getting Started” section with step‑by‑step commands (`pip install founder-launchpad`, `fl launch demo`, `fl sandbox run`).<br>- All commands in the guide succeed on a fresh Ubuntu 22.04 VM. |
| **E5‑S2** | **As a contributor, I want contribution guidelines and a code of conduct, so that I can safely submit PRs.** | - `CONTRIBUTING.md` outlines linting, testing, and release process.<br>- `CODE_OF_CONDUCT.md` follows the Contributor Covenant 2.0.<br>- CI checks enforce the guidelines on PRs. |
| **E5‑S3** | **As a community member, I want a set of example projects, so that I can see real‑world usage patterns.** | - `examples/` folder contains at least three starter apps (CLI tool, web API with FastAPI, data pipeline).<br>- Each example includes a README with run instructions and expected output.<br>- Tests validate that each example builds and runs via `fl sandbox run`. |

---

## Prioritisation Summary (MVP)

1. **E1‑S1 → E1‑S5** – Core scaffold, sandbox, config, help, CI.
2. **E2‑S1 → E2‑S4** – Testing, linting, type‑checking, release flow.
3. **E3‑S1** – Plugin entry‑point foundation (enables later plugins).
4. **E4‑S1** – Telemetry collection (lightweight, opt‑out).
5. **E5‑S1 → E5‑S3** – Documentation and examples to drive adoption.

Stories are ordered to deliver a usable, high‑quality product after the first release, then expand functionality and community support in subsequent sprints.
