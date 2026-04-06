# Django Commands

## manage.py

The project's `manage.py` is located at `src/myproject/manage.py`. You can run it directly:

```bash
python src/myproject/manage.py <command>
```

Or, after installing the project (`pip install -e .`), use the `manage` entry point:

```bash
manage <command>
```

This entry point is defined in `pyproject.toml` under `[project.scripts]`.

## Built-in Django Commands

| Command | Description |
|---------|-------------|
| `runserver` | Start the development server |
| `migrate` | Apply database migrations |
| `makemigrations` | Generate new migrations |
| `createsuperuser` | Create an admin user |
| `collectstatic` | Collect static files for production |
| `shell` | Open a Python shell with Django context |

## Django Extensions Commands

With `django-extensions` installed, you get additional commands:

| Command | Description |
|---------|-------------|
| `runserver_plus` | Enhanced dev server with Werkzeug debugger |
| `shell_plus` | Auto-imports all models in the shell |
| `show_urls` | Display all registered URL patterns |
| `reset_db` | Reset the database (use with caution!) |

## Custom Project Commands

### `seed_db`
Seeds the database with example development data.

```bash
python src/myproject/manage.py seed_db
```

Creates a test user and any other development fixtures.

### `health_check`
Verifies that required services (database, Redis) are reachable.

```bash
python src/myproject/manage.py health_check
```

## django-temporalio Commands

The `django-temporalio` package provides management commands for Temporal workflow orchestration:

### `start_temporalio_worker`
Starts a Temporal worker for a specific queue or all queues.

```bash
# Start the "main" worker (production)
python src/myproject/manage.py start_temporalio_worker main

# Start workers for all configured queues (development)
python src/myproject/manage.py start_temporalio_worker --all
```

### `show_temporalio_queue_registry`
Shows all registered activities and workflows per task queue.

```bash
python src/myproject/manage.py show_temporalio_queue_registry
```

### `sync_temporalio_schedules`
Syncs registered Temporal schedules with the Temporal server.

```bash
python src/myproject/manage.py sync_temporalio_schedules
```

## Docker Directory Structure

All infrastructure files live under `docker/` to keep the project root clean:

```
docker/
├── compose.yaml          # Development services
├── compose.prod.yaml     # Production override
├── Dockerfile            # Production multi-stage build
├── Dockerfile.dev        # Development image
├── nginx/
│   ├── nginx.conf        # Production reverse proxy
│   └── dev.conf          # Development proxy
└── scripts/
    ├── entrypoint.sh     # Container entrypoint
    ├── setup-env.sh      # Environment setup
    └── wait-for-it.sh    # TCP port waiter
```

The `Makefile` abstracts the Docker paths so you run `make dev` instead of `docker compose -f docker/compose.yaml up -d`.
