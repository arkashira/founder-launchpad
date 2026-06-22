# REQUIREMENTS.md

## 1. Overview
**Founder‑Launchpad** is a lightweight Python toolkit that enables early‑stage founders to spin‑up, validate, and iterate on product ideas with minimal boilerplate. This document defines the concrete requirements that the implementation must satisfy to be considered shippable and ready for validation in the Axentx pipeline.

---

## 2. Functional Requirements  

| ID | Description |
|----|-------------|
| **FR‑1** | **CLI Scaffold Generator** – Provide a `fl launch` command that creates a fully‑functional project skeleton (including `pyproject.toml`, `src/`, `tests/`, `.env.example`, and a starter `main.py`). The generated project must be runnable with `python -m founder_launchpad` and pass the built‑in test suite. |
| **FR‑2** | **Sandbox Runner** – Implement a `fl sandbox <script_path>` command that executes the supplied launch script inside an isolated virtual environment (venv) without affecting the host Python installation. The sandbox must automatically install any dependencies declared in a `requirements.txt` located next to the script. |
| **FR‑3** | **Config Manager** – Expose a `founder_launchpad.config` module that loads configuration from (in order of precedence) environment variables, a `.env` file, a YAML file (`config.yaml`), and a JSON file (`config.json`). The module must validate the merged configuration against a JSON‑Schema defined in `config_schema.json` and raise a descriptive `ConfigError` on mismatch. |
| **FR‑4** | **Telemetry Collector** – On each successful `fl launch` or `fl sandbox` execution, send an anonymous POST request to `https://telemetry.founder-launchpad.com/collect` containing: toolkit version, Python version, OS platform, and a hash of the command line (no user‑identifying data). Telemetry must be opt‑out via an environment variable `FL_TELEMETRY=0`. |
| **FR‑5** | **Plugin System** – Allow third‑party extensions to register new CLI sub‑commands via `setuptools` entry‑points under the group `founder_launchpad.plugins`. The core CLI must discover and expose these commands automatically (`fl <plugin‑command>`). |
| **FR‑6** | **CI Integration Boilerplate** – Provide a ready‑to‑use GitHub Actions workflow (`.github/workflows/ci.yml`) that runs: <br>1. `ruff` linting <br>2. `pytest` with coverage (minimum 95 %) <br>3. Build and publish a wheel to GitHub Packages on tag push. |
| **FR‑7** | **Error Reporting** – All uncaught exceptions in the toolkit must be captured, logged with stack trace, and re‑raised as a `FounderLaunchpadError` with a user‑friendly message suggesting next steps. |
| **FR‑8** | **Documentation Generation** – Expose a `fl docs` command that runs `mkdocs build` using the `mkdocs.yml` located at the repository root, producing a static site in `site/`. The command must fail if any markdown file contains broken links (checked via `mkdocs‑link‑check`). |
| **FR‑9** | **Versioning** – The package must expose `founder_launchpad.__version__` following Semantic Versioning (MAJOR.MINOR.PATCH). The CLI must display the version with `fl --version`. |
| **FR‑10** | **Testing Fixtures** – Provide a `founder_launchpad.testing` module containing pytest fixtures (`tmp_project`, `sandbox_env`) that can be imported by downstream projects to achieve ≥95 % coverage on starter templates. |

---

## 3. Non‑Functional Requirements  

| ID | Requirement |
|----|-------------|
| **NFR‑1** | **Performance** – Sandbox creation (venv + dependency install) must complete in ≤ 30 seconds for projects with ≤ 20 dependencies on a typical CI runner (2 vCPU, 4 GB RAM). |
| **NFR‑2** | **Security** – All external inputs (environment vars, config files, plugin code) must be validated before execution. The sandbox must run with `--no-site-packages` and without elevated privileges. |
| **NFR‑3** | **Reliability** – CLI commands must return a non‑zero exit code on any failure and produce a deterministic error message. Unit‑test suite must achieve ≥ 95 % line coverage and pass on Python 3.11, 3.12. |
| **NFR‑4** | **Scalability** – The plugin discovery mechanism must support loading ≥ 100 plugins without noticeable latency (> 200 ms) on startup. |
| **NFR‑5** | **Observability** – Logs must be emitted in JSON format to stdout with fields: timestamp, level, component, message, and optional `trace_id`. The default log level is `INFO`; can be overridden via `FL_LOG_LEVEL`. |
| **NFR‑6** | **Portability** – The toolkit must be pure Python (no compiled extensions) and installable on Windows, macOS, and Linux via `pip install founder-launchpad`. |
| **NFR‑7** | **Compliance** – The project must retain the MIT license header in every source file and include a `LICENSE` file. No third‑party code with incompatible licenses may be bundled. |
| **NFR‑8** | **Maintainability** – Codebase must follow the `ruff` style guide (PEP 8 + additional Axentx rules). All public APIs must have type hints and docstrings compliant with `pydocstyle`. |
| **NFR‑9** | **Telemetry Privacy** – Telemetry payload must be ≤ 256 bytes, contain no PII, and be transmitted over HTTPS with TLS 1.2+. Users must be able to disable it without rebuilding the package. |
| **NFR‑10** | **Documentation** – README, API reference (auto‑generated via `mkdocstrings`), and usage guides must be kept in sync with code; CI must fail if `mkdocs build` reports broken links or missing pages. |

---

## 4. Constraints  

1. **Language & Runtime** – Must target Python 3.11+; no reliance on deprecated stdlib modules.  
2. **Packaging** – Distribution format limited to a source distribution (`sdist`) and a binary wheel (`bdist_wheel`).  
3. **Dependency Policy** – Direct dependencies limited to ≤ 15 packages; each must be MIT, BSD, Apache‑2.0, or similarly permissive.  
4. **CI Environment** – All CI steps must run within GitHub‑hosted runners; no self‑hosted runners are permitted for the initial release.  
5. **Telemetry Endpoint** – Must be reachable without authentication; fallback to a no‑op stub if the endpoint is unreachable (to avoid blocking CLI execution).  

---

## 5. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Founders will run the toolkit on machines with internet access to fetch dependencies and telemetry. |
| **A‑2** | The target audience is comfortable with a terminal‑first workflow; no GUI is required for MVP. |
| **A‑3** | Users will have Python 3.11 or newer installed; the toolkit will not manage Python version installation. |
| **A‑4** | Plugin developers will publish their extensions to PyPI and declare entry‑points correctly. |
| **A‑5** | The telemetry service (`telemetry.founder-launchpad.com`) will accept POSTs without authentication and will handle rate‑limiting internally. |
| **A‑6** | The CI pipeline will have sufficient resources (2 vCPU, 4 GB RAM) to satisfy performance NFR‑1. |
| **A‑7** | All configuration schemas are static and can be expressed in a single JSON‑Schema file. |
| **A‑8** | The sandbox runner will use the system `python -m venv` module; no external virtual‑env managers (e.g., `conda`) are required. |

---  

*Prepared by the Senior Product/Engineering Lead, Axentx OS – Founder‑Launchpad project.*
