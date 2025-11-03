# Stage 1: build the front-end assets with the same toolchain used in development
FROM node:24.7-slim AS front-build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY _front ./_front
COPY vite.config.mjs ./

RUN npm run build

###

# Stage 2: build the Python application image
FROM python:3.13.7-slim AS runtime

WORKDIR /app

ENV DATABASE_URL=sqlite:///app.db \
    SECRET_KEY=change-me \
    PYDEVD_DISABLE_FILE_VALIDATION=1 \
    DJANGO_RUNSERVER_HIDE_WARNING=true \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKERED=1 \
    DJANGO_SETTINGS_MODULE=conf.settings.production \
    DEBUG=0 \
    PORT=80 \
    UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

COPY --from=front-build /app/_static /app/_static

RUN mkdir -p _logs _media _static_collected

EXPOSE 80

CMD ["gunicorn", \
     "--access-logfile", "/app/_logs/gunicorn_access.log", \
     "--log-level", "error", \
     "--workers", "3", \
     "--timeout", "10", \
     "--bind", "0.0.0.0:$PORT", \
     "--forwarded-allow-ips", "*", \
     "conf.wsgi:application"]
