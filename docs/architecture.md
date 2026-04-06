# Architecture

## Project Layout

This project uses a **src layout**: all Django code lives under `src/myproject/`. This prevents the common issue where `import myproject` resolves to the wrong directory during development.

```
src/myproject/
├── settings/           # Split settings (base → development/production)
├── core/               # Shared utilities: base models, middleware, context processors
├── accounts/           # Custom user model, API key auth
├── api/                # Django REST Framework endpoints
├── chat/               # HTMX chat interface + Django AI Assistant
├── workflows/          # Temporal workflow definitions
├── templates/          # Project-wide templates
└── static/             # CSS, JS, images (vendored HTMX)
```

## Settings Split

Settings are split into three files:

- **`base.py`** — Shared configuration. All values read from environment variables via `django-environ` with sensible defaults.
- **`development.py`** — Imports from base, enables DEBUG, debug toolbar, console email, relaxed CORS.
- **`production.py`** — Imports from base, enables SSL redirect, HSTS, secure cookies, WhiteNoise, Redis cache.

The `DJANGO_ENV` environment variable (default: `development`) controls which settings module is loaded. See `settings/__init__.py`.

## Authentication

The project supports **two authentication methods** that coexist:

1. **Session Authentication** — Used by the HTMX web interface. Users log in via `/accounts/login/`, Django sets a session cookie.
2. **API Key Authentication** — Used by external API consumers. Send `Authorization: Api-Key <key>` header. Keys are hashed (SHA-256) and stored. The raw key is shown only once at creation.

DRF is configured with both authentication backends, so any endpoint accepts either method.

## How HTMX and DRF Coexist

- **HTMX pages** (`/chat/`) use Django's standard views, templates, and session auth. HTMX makes partial page updates via POST requests that return HTML fragments.
- **DRF API** (`/api/v1/`) returns JSON. Uses the same models and business logic, different serialization layer.

Both share the same URL router (`urls.py`), same authentication, same database. The HTMX views and DRF views are in separate apps (`chat` and `api`) for clarity.

## App Responsibilities

| App | Purpose |
|-----|---------|
| `core` | Base model classes (TimeStampedModel, UUIDModel), middleware (request ID, timing), context processors |
| `accounts` | Custom User model, API key model, authentication backend, login/logout views |
| `api` | DRF viewsets, serializers, throttling. Serves `/api/v1/` |
| `chat` | HTMX chat interface, Django AI Assistant integration |
| `workflows` | Temporal activities and workflows for async processing |

## Temporal Integration

The `workflows` app integrates with Temporal via `django-temporalio`. Key concepts:

- **Activities** (in `activities.py`) — Individual units of work. Registered on task queues.
- **Workflows** (in `workflows.py`) — Orchestrate activities with retry logic, timeouts, etc.
- **Workers** — Long-running processes that poll queues and execute activities/workflows. Started via `manage start_temporalio_worker`.
- **Signals** (in `signals.py`) — Django signals can trigger workflows. Example: post-processing chat messages.

The `BASE_MODULE` setting tells `django-temporalio` where to auto-discover activities and workflows (files matching `*activities*.py` and `*workflows*.py`).

## Static Files

- **Development:** Django serves static files directly from `src/myproject/static/`.
- **Production:** `collectstatic` gathers files into a Docker volume. Nginx serves `/static/` from the volume. WhiteNoise is configured as a fallback.
