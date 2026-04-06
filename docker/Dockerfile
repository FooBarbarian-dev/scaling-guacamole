# Production Dockerfile — multi-stage build
FROM python:3.13-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

# Copy application code
COPY . .

# Set ownership
RUN chown -R appuser:appuser /app

# Create staticfiles directory
RUN mkdir -p /app/staticfiles && chown appuser:appuser /app/staticfiles

ENV DJANGO_ENV=production
ENV STATIC_ROOT=/app/staticfiles
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

CMD ["bash", "docker/scripts/entrypoint.sh"]
