# My Project

<!-- TODO: Replace with your project name and description -->

> A production-ready Django project with REST API, HTMX chat interface, AI assistant integration, and Temporal workflow orchestration.

<!-- TODO: Add badges (CI, coverage, license) -->

## Prerequisites

- Python 3.13+
- Docker & Docker Compose
- Conda (optional, for local development without Docker)

## Quickstart

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd myproject
   ```

2. **Set up environment variables:**
   ```bash
   make setup-env
   # Or manually: cp .env.example .env and edit values
   ```

3. **Start development services:**
   ```bash
   make dev
   ```

4. **Run migrations:**
   ```bash
   make migrate
   ```

5. **Create a superuser:**
   ```bash
   make superuser
   ```

Visit http://localhost:8000/admin/ to access the admin panel, or http://localhost:8000/chat/ for the chat interface.

## Creating Your First Admin User

```bash
# Via Docker
docker compose -f docker/compose.yaml exec web python src/myproject/manage.py createsuperuser

# Or locally (with virtualenv/conda activated)
python src/myproject/manage.py createsuperuser
```

## Creating API Keys

**Via Admin Panel:**
1. Log in to http://localhost:8000/admin/
2. Go to Accounts > API Keys > Add API Key
3. Or go to a User's detail page and add an API key inline

**Via Django Shell:**
```bash
make shell
```
```python
from myproject.accounts.models import User, APIKey
user = User.objects.get(username="admin")
raw_key, api_key = APIKey.create_key(user=user, name="My API Key")
print(f"API Key (save this, shown only once): {raw_key}")
```

**Using the API Key:**
```bash
curl -H "Authorization: Api-Key YOUR_KEY_HERE" http://localhost:8000/api/v1/chat/sessions/
```

## Development

### Running Tests
```bash
make test
```

### Linting
```bash
make lint
```

### Adding New Apps
```bash
cd src/myproject
python manage.py startapp your_app_name
```
Then add `"myproject.your_app_name"` to `INSTALLED_APPS` in `src/myproject/settings/base.py`.

### Useful Commands
```bash
make shell          # Django shell_plus
make migrate        # Run migrations
make makemigrations # Generate migrations
make seed           # Seed development data
make collectstatic  # Collect static files
make clean          # Remove containers and caches
```

## Production Deployment

```bash
# Build and start production services (includes nginx)
make prod

# Or manually:
docker compose -f docker/compose.yaml -f docker/compose.prod.yaml up -d --build
```

See [docs/production-vs-dev.md](docs/production-vs-dev.md) for details on what differs between environments.

## API Documentation

- **Swagger UI:** http://localhost:8000/api/v1/docs/
- **ReDoc:** http://localhost:8000/api/v1/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/v1/schema/

## Project Structure

```
src/myproject/          # Django project root
├── settings/           # Split settings (base, development, production)
├── core/               # Shared utilities, base models, middleware
├── accounts/           # User management, API key authentication
├── api/                # DRF REST API
├── chat/               # HTMX chat interface with AI assistant
└── workflows/          # Temporal workflow orchestration
```

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Documentation

- [Quickstart Guide](docs/quickstart.md)
- [Architecture](docs/architecture.md)
- [Django Commands](docs/django-commands.md)
- [AI Assistant Setup](docs/ai-assistant-setup.md)
- [Production vs Development](docs/production-vs-dev.md)
- [Services](docs/services.md)
- [Environment Variables](docs/env-variables.md)

<!-- TODO: Add project-specific sections as needed -->
