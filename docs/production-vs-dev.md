# Production vs Development

## Settings Comparison

| Setting | Development | Production |
|---------|------------|------------|
| `DEBUG` | `True` | `False` |
| `ALLOWED_HOSTS` | `["*"]` | From `ALLOWED_HOSTS` env var |
| `CORS` | `CORS_ALLOW_ALL_ORIGINS = True` | Explicit `CORS_ALLOWED_ORIGINS` list |
| `SECURE_SSL_REDIRECT` | `False` | `True` |
| `SESSION_COOKIE_SECURE` | `False` | `True` |
| `CSRF_COOKIE_SECURE` | `False` | `True` |
| `HSTS` | Disabled | 1 year, include subdomains, preload |
| `Email` | Console backend | Configure SMTP |
| `Cache` | Local memory (default) | Redis |
| `DB connections` | Default | Pooled (`CONN_MAX_AGE=600`) |

## Docker Configurations

| Aspect | Development (`compose.yaml`) | Production (`compose.prod.yaml`) |
|--------|------------------------------|----------------------------------|
| **Dockerfile** | `Dockerfile.dev` (single stage, debugpy) | `Dockerfile` (multi-stage, non-root user) |
| **Server** | `runserver_plus` (Werkzeug hot reload) | `gunicorn` (multi-worker) |
| **Static files** | Django serves directly | `collectstatic` → shared volume → nginx |
| **Source code** | Mounted as volume (hot reload) | Copied into image |
| **Debug tools** | Debug toolbar, debugpy (port 5678) | None |
| **Temporal UI** | Available on port 8080 | Behind `debug` profile |
| **nginx** | Not included | Serves static files + reverse proxy |

## Static File Serving

### Development
Django's built-in static file serving handles all static assets. No `collectstatic` needed. Files are served directly from `src/myproject/static/`.

### Production
1. `entrypoint.sh` runs `collectstatic --noinput` at container start
2. Collected files go to `/app/staticfiles` (a named Docker volume)
3. The `staticfiles` volume is shared between the `web` and `nginx` containers
4. Nginx serves `/static/` directly from the volume
5. WhiteNoise is configured as a fallback in Django middleware

## Debug Tools

### Development Only
- **Django Debug Toolbar** — SQL queries, templates, cache, signals
- **debugpy** — Remote debugging from VS Code/Zed (port 5678)
- **runserver_plus** — Werkzeug interactive debugger on errors
- **shell_plus** — Auto-imports all models

### Both Environments
- `/health/` endpoint — Returns `{"status": "ok"}`
- `manage health_check` — Verifies database and Redis connectivity
- Structured logging with request IDs
