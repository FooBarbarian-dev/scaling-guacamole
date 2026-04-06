# Environment Variables

All environment variables used by the project, with their purpose, default values, and whether they are required.

| Variable | Purpose | Default | Required |
|----------|---------|---------|----------|
| `DJANGO_ENV` | Environment selector (`development` or `production`) | `development` | No |
| `SECRET_KEY` | Django secret key for cryptographic signing | `django-insecure-change-me-in-production` | **Yes (prod)** |
| `DEBUG` | Enable Django debug mode | `False` | No |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://myproject:myproject@localhost:5432/myproject` | No |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` | No |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | `localhost,127.0.0.1,0.0.0.0` | **Yes (prod)** |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | `http://localhost:3000,http://localhost:8000` | **Yes (prod)** |
| `AI_ASSISTANT_OPENAI_API_BASE` | OpenAI-compatible API base URL (or vLLM URL) | `https://api.openai.com/v1` | No |
| `AI_ASSISTANT_OPENAI_API_KEY` | API key for the AI assistant | _(empty)_ | **Yes** |
| `AI_ASSISTANT_MODEL` | Model name for the AI assistant | `gpt-4o` | No |
| `TEMPORALIO_HOST` | Temporal server host:port | `localhost:7233` | No |
| `TEMPORALIO_TASK_QUEUE` | Default Temporal task queue name | `main-task-queue` | No |
| `ENABLE_TEMPORAL_POST_PROCESSING` | Enable Temporal workflow on chat message save | `False` | No |
| `EMAIL_BACKEND` | Django email backend class | `django.core.mail.backends.console.EmailBackend` | No |
| `GUNICORN_WORKERS` | Number of Gunicorn worker processes (prod) | `2 * CPU + 1` | No |

## Notes

- **`SECRET_KEY`**: In development, a default insecure key is provided. **You must set a secure key in production.** Generate one with:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- **`DATABASE_URL`**: Uses the `dj-database-url` format via `django-environ`. Examples:
  - PostgreSQL: `postgres://user:pass@host:5432/dbname`

- **`CORS_ALLOWED_ORIGINS`**: In development, `CORS_ALLOW_ALL_ORIGINS=True` overrides this. In production, you must provide explicit origins.

- **`AI_ASSISTANT_OPENAI_API_BASE`**: For vLLM, set to `http://your-vllm-server:8000/v1`. For Azure OpenAI, set to your Azure endpoint.

- **`AI_ASSISTANT_OPENAI_API_KEY`**: For vLLM, use `EMPTY` if no authentication is configured.
