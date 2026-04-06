#!/usr/bin/env bash
set -euo pipefail

ENV_FILE=".env"
EXAMPLE_FILE=".env.example"

if [ -f "$ENV_FILE" ]; then
    echo ".env file already exists. Remove it first if you want to regenerate."
    exit 0
fi

if [ ! -f "$EXAMPLE_FILE" ]; then
    echo "Error: $EXAMPLE_FILE not found."
    exit 1
fi

echo "Setting up environment file..."
cp "$EXAMPLE_FILE" "$ENV_FILE"

# Generate a random SECRET_KEY
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>/dev/null || openssl rand -base64 50 | tr -d '\n/+=')
sed -i "s|change-me-to-a-random-secret-key|${SECRET_KEY}|g" "$ENV_FILE"

echo ""
echo "Generated .env file with a random SECRET_KEY."
echo ""
echo "Review and update the following values in .env:"
echo "  - DATABASE_URL (default: postgres://myproject:myproject@localhost:5432/myproject)"
echo "  - AI_ASSISTANT_OPENAI_API_KEY (TODO: set your API key)"
echo "  - AI_ASSISTANT_MODEL (default: gpt-4o)"
echo "  - CORS_ALLOWED_ORIGINS (for production)"
echo ""
echo "Done! Run 'make dev' to start development services."
