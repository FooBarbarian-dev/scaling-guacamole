# Services

## Docker Compose Services

### Development (`docker/compose.yaml`)

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `postgres` | `postgres:18` | 5432 | PostgreSQL database |
| `redis` | `redis:8-alpine` | 6379 | Cache and message broker |
| `temporalio` | `temporalio/auto-setup` | 7233 | Temporal server |
| `temporalio-ui` | `temporalio/ui` | 8080 | Temporal Web UI |
| `web` | Built from `Dockerfile.dev` | 8000 | Django development server |
| `temporal-worker` | Built from `Dockerfile.dev` | — | Temporal worker process |

### Production Additions (`docker/compose.prod.yaml`)

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `nginx` | `nginx:alpine` | 80 | Reverse proxy + static files |
| `web` | Built from `Dockerfile` | 8000 (internal) | Gunicorn application server |

## Accessing UIs

- **Django Admin:** http://localhost:8000/admin/
- **Chat Interface:** http://localhost:8000/chat/
- **Swagger API Docs:** http://localhost:8000/api/v1/docs/
- **ReDoc:** http://localhost:8000/api/v1/redoc/
- **Temporal UI:** http://localhost:8080/
- **Health Check:** http://localhost:8000/health/

## The `staticfiles` Volume

In production, static files are shared between the `web` and `nginx` containers via a named Docker volume called `staticfiles`:

1. The `web` container runs `collectstatic --noinput` at startup (in `entrypoint.sh`)
2. Collected files are written to `/app/staticfiles` inside the container
3. This path is backed by the `staticfiles` named volume
4. The `nginx` container mounts the same volume at `/usr/share/nginx/static`
5. Nginx serves `/static/` directly from this mount point

### Updating Static Assets

To update logos, favicons, or other static files:

1. Replace the files in `src/myproject/static/img/` (or relevant directory)
2. Rebuild and restart: `make prod`
3. The entrypoint runs `collectstatic` which copies new files to the volume
4. Nginx serves the updated files immediately

## PostgreSQL 18 Note

PostgreSQL 18 changed the default data directory location. The named volume is mounted at `/var/lib/postgresql` (not the old `/var/lib/postgresql/data`), and `PGDATA` is set explicitly to `/var/lib/postgresql/18/docker`. See the comment in `docker/compose.yaml`.

## Redis 8 Note

Redis 8+ uses a tri-license model (RSALv2/SSPLv1/AGPLv3). Evaluate license compatibility for your use case.
