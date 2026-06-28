```markdown
# Tech Spec: Founder Launchpad

## Stack
- **Language**: Python 3.11
- **Framework**: FastAPI 0.104.1
- **Runtime**: Dockerized with uvicorn ASGI server
- **Frontend**: React 18 with TypeScript
- **Database**: PostgreSQL 15 (via Supabase for managed DB)
- **Authentication**: Supabase Auth (JWT-based)
- **Caching**: Redis 7 (for session caching)
- **Task Queue**: Celery 5.3 with Redis backend
- **Infrastructure**: Terraform 1.5+ for IaC

## Hosting
- **Primary Platform**: Render.com (free tier first)
- **Database**: Supabase (managed Postgres)
- **Static Assets**: Vercel (for frontend)
- **CDN**: Cloudflare (for global distribution)
- **Monitoring**: Datadog (free tier)

## Data Model
### Tables/Collections
1. **users**
   - id (UUID, PK)
   - email (string, unique)
   - created_at (timestamp)
   - updated_at (timestamp)
   - profile_data (JSONB)

2. **projects**
   - id (UUID, PK)
   - owner_id (UUID, FK users.id)
   - name (string)
   - description (text)
   - status (enum: draft, launched, archived)
   - created_at (timestamp)
   - updated_at (timestamp)
   - config (JSONB)

3. **project_templates**
   - id (UUID, PK)
   - name (string)
   - description (text)
   - template_config (JSONB)
   - created_at (timestamp)
   - updated_at (timestamp)

4. **launch_attempts**
   - id (UUID, PK)
   - project_id (UUID, FK projects.id)
   - status (enum: pending, success, failed)
   - logs (text)
   - created_at (timestamp)
   - completed_at (timestamp)

### Key Fields
- Primary keys: UUIDs for all entities
- Foreign keys: Properly indexed relationships
- Timestamps: All tables have created_at and updated_at

## API Surface
1. **POST /api/auth/signup** - User registration
2. **POST /api/auth/login** - User authentication
3. **GET /api/users/profile** - Get user profile
4. **PUT /api/users/profile** - Update user profile
5. **GET /api/projects** - List user projects
6. **POST /api/projects** - Create new project
7. **GET /api/projects/{id}** - Get project details
8. **PUT /api/projects/{id}** - Update project
9. **DELETE /api/projects/{id}** - Archive project
10. **POST /api/projects/{id}/launch** - Trigger project launch

## Security Model
- **Authentication**: JWT tokens via Supabase Auth
- **Authorization**: Role-based access control (RBAC) with user roles
- **Secrets Management**: Environment variables via Render secrets
- **IAM**: Supabase Auth handles identity management
- **Data Encryption**: HTTPS/TLS in transit, encrypted storage at rest
- **Rate Limiting**: API rate limiting via FastAPI middleware
- **Input Validation**: Pydantic models for all request/response bodies

## Observability
- **Logging**: Structured logging with JSON format using structlog
- **Metrics**: Prometheus metrics exposed via FastAPI middleware
- **Tracing**: OpenTelemetry integration with Datadog exporter
- **Error Tracking**: Sentry for error monitoring
- **Health Checks**: /health endpoint returning 200 OK
- **Performance Monitoring**: Built-in FastAPI performance metrics

## Build/CI
- **Build System**: Poetry 1.5 for dependency management
- **Testing**: pytest 7.4 with coverage.py
- **CI Pipeline**: GitHub Actions workflows
- **Code Quality**: Black, flake8, mypy pre-commit hooks
- **Deployment**: Automated deployment on Render via GitHub Actions
- **Versioning**: Semantic versioning with Git tags
- **Documentation**: Swagger/OpenAPI docs generated automatically
```