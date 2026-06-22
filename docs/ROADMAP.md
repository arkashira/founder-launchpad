# ROADMAP.md

## 🎯 Vision
Empower solo founders and early‑stage teams to spin up, validate, and iterate on product ideas **without writing boilerplate**. The roadmap balances rapid time‑to‑value (MVP) with a sustainable, extensible platform that can grow into a full‑featured launch ecosystem.

---

## 📅 Milestones

| Milestone | Target Release | Description | MVP‑Critical |
|-----------|----------------|-------------|--------------|
| **MVP – Launch‑Ready Sandbox** | **2026‑07‑15** | Core toolkit that lets a founder run `fl launch` and get a working prototype in < 5 min. | ✅ |
| **v1 – Founder‑Workflow Suite** | 2026‑10‑01 | Add end‑to‑end workflow helpers (idea validation, MVP metrics, one‑click deployment). | — |
| **v2 – Marketplace & Collaboration** | 2027‑02‑15 | Plugin marketplace, team collaboration features, and advanced telemetry dashboards. | — |

---

## 🚀 MVP (Must‑Have for Launch)

| Feature | Scope | Acceptance Criteria |
|---------|-------|----------------------|
| **CLI Scaffolding** | `fl launch <project-name>` generates a ready‑to‑run Python project with sensible defaults. | - Project skeleton created in < 2 seconds.<br>- Includes `main.py`, `pyproject.toml`, `.env.example`, and a basic test file.<br>- Passes `flake8` and `pytest` out‑of‑the‑box. |
| **Sandbox Runner** | Executes the generated project inside an isolated virtual environment (venv). | - Spins up venv, installs dependencies, runs `python -m src.main`.<br>- Captures stdout/stderr and returns a structured JSON result.<br>- Clean‑up on completion or failure. |
| **Config Manager** | Unified handling of `.env`, YAML, and JSON with Pydantic validation. | - Auto‑detects config file type.<br>- Provides `config.load()` that returns a typed object.<br>- Errors are displayed with line‑number hints. |
| **Basic Telemetry** | Anonymous usage ping (launch count, OS, Python version). | - Opt‑out via `FL_TELEMETRY=0` env var.<br>- Sends data to the existing Axentx telemetry endpoint. |
| **CI Integration** | Pre‑configured GitHub Actions workflow for lint, test, and release. | - Workflow runs on every push.<br>- Fails on < 95 % coverage or lint errors.<br>- Publishes a GitHub Release on tag push. |
| **Documentation & Quick‑Start** | README, `docs/quickstart.md`, and generated API reference via MkDocs. | - New user can follow the guide and have a running prototype in < 5 min.<br>- Docs build passes CI. |

*All MVP items are **shippable** within a single sprint (2 weeks) by the core dev team.*

---

## 🌱 v1 – Founder‑Workflow Suite

| Theme | Features | Target Release |
|-------|----------|----------------|
| **Idea Validation** | - Prompt‑driven market‑signal fetcher (leverages Axentx BRAIN).<br>- One‑click “run validation” that returns a **pain‑score** and **WTP** estimate.<br>- Exportable validation report (PDF/HTML). | 2026‑10‑01 |
| **MVP Metrics** | - Built‑in health checks (latency, error rate).<br>- Simple analytics dashboard (Flask + Chart.js) served locally.<br>- Export to CSV/JSON for investor decks. | 2026‑10‑01 |
| **One‑Click Deployment** | - Deploy to Fly.io, Vercel, or Docker Hub via `fl deploy`.<br>- Auto‑generated Dockerfile & CI step.<br>- Rollback command. | 2026‑10‑01 |
| **Extensible Plugin SDK** | - Formal entry‑point spec (`founder_launchpad.plugins`).<br>- Sample plugins: Slack notifier, Stripe integration.<br>- Plugin registry CLI (`fl plugins list/install`). | 2026‑10‑01 |
| **Enhanced Testing** | - Pytest fixtures for sandbox, config, and telemetry mocks.<br>- Coverage badge auto‑update in README. | 2026‑10‑01 |

**Success Metrics for v1**  
- ≥ 1 000 active installations (tracked via telemetry).  
- Average prototype spin‑up time ≤ 3 minutes.  
- ≥ 70 % of users run at least one validation or deployment command.

---

## 🌐 v2 – Marketplace & Collaboration

| Theme | Features | Target Release |
|-------|----------|----------------|
| **Plugin Marketplace** | - Web UI (FastAPI + React) to browse, rate, and install community plugins.<br>- Secure sandboxed execution of third‑party plugins.<br>- Revenue‑share model for premium plugins. | 2027‑02‑15 |
| **Team Collaboration** | - Multi‑user workspaces with role‑based access (founder, dev, reviewer).<br>- Shared sandbox sessions & live logs.<br>- Commenting & issue linking directly from the CLI. | 2027‑02‑15 |
| **Advanced Telemetry & Insights** | - Dashboard with cohort analysis, funnel conversion, and churn prediction (leveraging Axentx BRAIN).<br>- Export to CSV/Google Sheets.<br>- GDPR‑compliant data controls. | 2027‑02‑15 |
| **Custom Deployment Targets** | - First‑class support for Kubernetes, AWS Lambda, and Cloudflare Workers.<br>- Declarative `fl deploy --target <name>` syntax.<br>- Auto‑scaling config templates. | 2027‑02‑15 |
| **Enterprise‑Ready Packaging** | - Signed wheels, SSO integration, and audit logs.<br>- White‑label branding for incubators/accelerators. | 2027‑02‑15 |

**Success Metrics for v2**  
- Marketplace hosts ≥ 30 plugins with ≥ 5 k total downloads.  
- ≥ 200 teams using collaborative workspaces.  
- Revenue from premium plugins covers ≥ 30 % of operating costs.

---

## 📌 How We’ll Deliver

1. **Iterative Sprint Cycle** – 2‑week sprints, each ending with a shippable increment.  
2. **Feature Flags** – All v1/v2 features gated behind flags; can be toggled on/off for early adopters.  
3. **Continuous Validation** – Every new feature runs through the Axentx validation loop (pain‑score + willingness‑to‑pay) before PR merge.  
4. **Community Feedback Loop** – Early‑access beta channel (GitHub Discussions) to capture real‑world usage and prioritize fixes.

---

## 📈 Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Scope creep in MVP** | Delayed launch, diluted value | Strict “MVP‑Critical” label; any non‑critical item moves to v1. |
| **Telemetry privacy concerns** | User churn | Opt‑out flag, clear privacy policy, minimal data collection. |
| **Plugin security** | Platform compromise | Sandbox execution, signed plugins, review process before marketplace listing. |
| **Dependency churn** (e.g., fast‑changing CI tools) | Build failures | Pin major versions, maintain a `requirements.lock` file, automated dependency update bot. |

---

## 📚 References

- **[decisions/tech-stack.md]** – Full stack specification.  
- **[docs/quickstart.md]** – Current onboarding flow (MVP baseline).  
- **[CONTRIBUTING.md]** – Guidelines for plugin developers.  

--- 

*Prepared by the Founder‑Launchpad product team, 2026‑06‑22.*
