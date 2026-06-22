# TECH_SPEC.md  

**Project:** founder‑launchpad  
**Owner:** Axentx OS – Product Engineering  
**Version:** 1.0.0 (initial)  
**Last Updated:** 2026‑06‑22  

---  

## 1. Overview  

Founder‑Launchpad is a **lightweight, opinionated Python toolkit** that enables early‑stage founders to spin up a fully‑functional prototype (sandbox) in under five minutes, iterate rapidly, and ship with minimal boilerplate. The system is built around three core concepts:

1. **Sandbox Runner** – Executes a user‑provided launch script inside an isolated, reproducible virtual environment.  
2. **CLI Scaffolder** – Generates a ready‑to‑run project skeleton (`fl launch`).  
3. **Plugin Architecture** – Extensible command set via `setuptools` entry‑points, allowing custom data sources, deployment targets, or analytics modules.

All components are packaged as a single pip‑installable distribution (`founder-launchpad`) with zero‑runtime external services (except optional telemetry).  

---  

## 2. Architecture Diagram  

```
+-------------------+        +-------------------+        +-------------------+
|   CLI (fl launch) | ----> |   Core Engine     | ----> |   Sandbox Runner  |
+-------------------+        +-------------------+        +-------------------+
          |                         |                           |
          |                         |                           |
          v                         v                           v
+-------------------+   +-------------------+   +-------------------+
|   Config Manager  |   |   Plugin Loader   |   |   VirtualEnv (venv)|
+-------------------+   +-------------------+   +-------------------+
          |                         |                           |
          v                         v                           v
+-------------------+   +-------------------+   +-------------------+
|   Telemetry (opt) |   |   User Commands   |   |   Execution Log   |
+-------------------+   +-------------------+   +-------------------+
```

*Arrows denote data/control flow.*  

---  

## 3. Core Components  

| Component | Responsibility | Key Classes / Functions | Public API |
|-----------|----------------|--------------------------|------------|
| **CLI Interface** | Parse user commands, invoke scaffolding or run actions. | `cli.main`, `cli.generate_project`, `cli.run_sandbox` | `fl launch`, `fl run`, `fl plugin add` |
| **Config Manager** | Load, validate, and expose configuration from `.env`, YAML, JSON. | `config.Loader`, `config.SchemaValidator` | `config.load(path) → dict` |
| **Sandbox Runner** | Create isolated `venv`, install dependencies, execute user script, capture stdout/stderr. | `sandbox.Environment`, `sandbox.Executor` | `sandbox.run(script_path, env_vars) → RunResult` |
| **Plugin System** | Discover and register plugins via `entry_points` group `founder_launchpad.plugins`. | `plugin.PluginBase`, `plugin.Registry` | `plugin.register(name, Callable)` |
| **Telemetry (opt.)** | Emit anonymous usage events (command, duration, success). | `telemetry.Client` | `telemetry.emit(event_name, payload)` |
| **Logging** | Structured JSON logs for CI integration and debugging. | `log.Logger` (wrapper around `structlog`) | `log.get_logger(name)` |
| **Error Handling** | Unified exception hierarchy, user‑friendly messages, exit codes. | `errors.*` (e.g., `SandboxError`, `ConfigError`) | raise appropriate subclass |

---  

## 4. Data Model  

The toolkit stores **no persistent state** beyond optional telemetry. All runtime data is represented in memory:

```python
class RunResult:
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    env_snapshot: dict[str, str]   # environment variables used
```

Configuration schemas are defined using **pydantic** models:

```python
class AppConfig(BaseModel):
    name: str
    version: str = "0.1.0"
    env: dict[str, str] = {}
    dependencies: list[str] = []
```

Plugins expose a **Command** contract:

```python
class PluginBase(Protocol):
    name: str
    description: str
    def run(self, args: Namespace, config: dict) -> int: ...
```

---  

## 5. Key APIs / Interfaces  

### 5.1 Python Package API  

```python
# Public entry points
from founder_launchpad.cli import main as cli_main
from founder_launchpad.config import load as load_config
from founder_launchpad.sandbox import run as run_sandbox
from founder_launchpad.plugin import Registry as PluginRegistry
```

### 5.2 CLI Specification  

| Sub‑command | Syntax | Description |
|-------------|--------|-------------|
| `fl launch <project_name>` | `fl launch my‑app` | Generates a new project skeleton under `my‑app/`. |
| `fl run <script>` | `fl run ./my‑app/launch.py` | Executes the script in a sandbox; prints a summary table. |
| `fl plugin add <module:attr>` | `fl plugin add mypkg.myplugin:MyPlugin` | Registers a plugin at runtime (also persisted via `pyproject.toml`). |
| `fl telemetry on|off` | `fl telemetry off` | Enable/disable anonymous telemetry. |

All commands return **exit code 0** on success, non‑zero on failure, and emit structured logs to `stderr`.  

### 5.3 Plugin Registration (pyproject.toml)  

```toml
[project.entry-points."founder_launchpad.plugins"]
my_plugin = "mypkg.myplugin:MyPlugin"
```

The `PluginRegistry` loads these at import time and makes them available to the CLI via `fl plugin list`.  

---  

## 6. Technology Stack  

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | Python | >=3.11 | Modern syntax, pattern matching, performance. |
| Packaging | Poetry | 1.8.2 | Deterministic builds, lockfile. |
| Virtual Env | `venv` (std lib) | N/A | No external dependencies, reproducible. |
| Config Validation | Pydantic | 2.7 | Fast, type‑safe schema enforcement. |
| CLI Framework | Typer | 0.12 | Simple, auto‑generated docs, Click‑compatible. |
| Logging | structlog + loguru | 24.1 / 0.7 | Structured JSON + easy dev output. |
| Telemetry | Segment (optional) | 2.3 | Lightweight HTTP POST, respects GDPR. |
| Testing | pytest | 8.2 | Rich fixtures, coverage plugins. |
| CI/CD | GitHub Actions | – | Pre‑configured lint, test, release pipelines. |
| Lint/Format | ruff, black, isort | 0.6 / 24.3 / 5.13 | Fast static analysis, consistent style. |

All dependencies are MIT or Apache‑2.0 licensed; see `pyproject.toml` for the full list.  

---  

## 7. Dependencies  

| Dependency | Scope | License |
|------------|-------|---------|
| `typer[all]` | Runtime | MIT |
| `pydantic` | Runtime | MIT |
| `structlog` | Runtime | BSD‑3 |
| `loguru` | Runtime | MIT |
| `python-dotenv` | Runtime | BSD‑3 |
| `rich` | Runtime (CLI output) | MIT |
| `segment-analytics-python` | Optional telemetry | MIT |
| `pytest`, `pytest-cov` | Test | MIT |
| `ruff`, `black`, `isort` | Dev | MIT |
| `tomli` | Runtime (pyproject parsing) | MIT |

---  

## 8. Deployment & Distribution  

1. **Build** – `poetry build` produces a wheel (`founder_launchpad-1.0.0-py3-none-any.whl`).  
2. **Publish** – Automated GitHub Action pushes the wheel to **PyPI** on tag creation (`v*`).  
3. **Installation** – End‑users run `pip install founder-launchpad`.  
4. **Runtime** – No external services required; optional telemetry can be disabled via `FL_TELEMETRY=0` environment variable or `fl telemetry off`.  

The sandbox runner creates a **temporary `venv` directory** under the system temp folder (`$TMPDIR/founder-launchpad-sandbox-<uuid>`). It is automatically cleaned up after execution unless `--keep-env` flag is supplied (debug mode).  

---  

## 9. Security & Compliance  

| Concern | Mitigation |
|---------|------------|
| **Code Execution** | Sandbox runs in a separate `venv` with no network access by default (`--no-network` flag). Users can explicitly enable network via `--allow-network`. |
| **Dependency Safety** | `poetry lock` pins exact versions; CI runs `pip-audit` on the generated wheel. |
| **Telemetry Privacy** | Only non‑identifying usage events (command name, duration, success). No IP or project data. Users can opt‑out at any time. |
| **License Compatibility** | All transitive dependencies are MIT/Apache/BSD; repository includes `LICENSE` file and SPDX headers. |
| **Supply‑Chain** | GitHub Actions use pinned action versions; Docker build (if any) uses `python:3.11-slim` with digest. |

---  

## 10. Testing Strategy  

| Test Type | Tool | Coverage Goal |
|-----------|------|---------------|
| Unit | pytest + fixtures | 95 % |
| Integration (sandbox end‑to‑end) | pytest + `subprocess` | 90 % |
| CLI (click‑testing) | typer.testing.CliRunner | 100 % command coverage |
| Lint/Static | ruff, mypy (optional) | 0 warnings |
| Security | pip-audit, bandit | No high severity findings |

All tests live under `tests/` and are executed on every PR via the GitHub Actions workflow `ci.yml`.  

---  

## 11. Future Extensions (Roadmap)  

| Milestone | Feature | Impact |
|-----------|---------|--------|
| **v1.1** | Cloud sandbox (Docker‑based) | Enables reproducible Linux containers for non‑Python dependencies. |
| **v1.2** | Web UI scaffolder (FastAPI + HTMX) | Gives founders a one‑click web front‑end. |
| **v2.0** | Marketplace for community plugins | Encourages ecosystem growth, aligns with Axentx’s “plug‑and‑play” vision. |

---  

## 12. Glossary  

- **Sandbox** – Isolated execution environment (Python `venv`) used to run a founder’s prototype safely.  
- **Plugin** – Dynamically loaded command adhering to `PluginBase`; registered via `entry_points`.  
- **Telemetry** – Optional anonymous usage reporting to help the maintainers improve the toolkit.  

---  

*Prepared by the Founder‑Launchpad Engineering Lead – Axentx OS*
