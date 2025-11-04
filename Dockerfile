# Stage 1: build the front-end assets with the same toolchain used in development
FROM node:24.7-slim AS front

WORKDIR /app
# copy only lockfiles first for reproducible, cached installs
COPY package.json package-lock.json ./

# try npm ci for reproducible installs; fall back to npm install on Node versions
# where `npm ci` isn't available (some Node 24/npm combos). Keep cache mount.
RUN --mount=type=cache,target=/root/.npm \
    set -ex && (npm ci || npm install)

# copy templates needed by tailwind and frontend source, then build
# copying `templates/` after `npm ci` preserves the dependency cache
COPY templates ./templates
COPY _front ./_front
COPY vite.config.mjs ./

RUN npm run build

###

# Stage 2: build the Python application image
FROM python:3.13.7-slim AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gettext tzdata locales ca-certificates \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Configure timezone and locale
RUN echo "America/Sao_Paulo" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="pt_BR.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8

# Set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set production environment
ENV LANG="pt_BR.UTF-8" \
    LC_ALL="pt_BR.UTF-8" \
    DJANGO_SETTINGS_MODULE="conf.settings.production" \
    DOCKERIZED=True \
    DEBUG=False

# NOTE: avoid baking secrets (SECRET_KEY, SENTRY_DSN, DB URLs) into the image.
# Provide them at runtime via environment variables / secrets management.
ENV DATABASE_URL="sqlite:///app.db" \
    SENTRY_DSN="https://0000000000000000000000000000000@000000000000000000.ingest.us.sentry.io/0000000000000000" \
    SECRET_KEY="change-me" \
    UV_LINK_MODE="copy"

# Copy the 'uv' tool from the upstream image (requires BuildKit and support for
# --mount and --from referencing images). Keep this as-is but be aware BuildKit is
# required when building this Dockerfile.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM base AS build

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# copy application source and the built frontend static files
COPY . .
COPY --from=front /app/_static /app/_static

# collectstatic and compilemessages in a single layer
RUN uv run manage.py collectstatic --clear --noinput \
    && uv run manage.py compilemessages --ignore /app/.venv/

FROM base

# create unprivileged user and copy app as root (chown during copy)
RUN useradd -ms /bin/bash app
COPY --from=build --chown=app:app /app /app

# ensure virtualenv bin is on PATH
ENV PATH="/app/.venv/bin:$PATH"

# switch to non-root user for runtime
USER app:app

EXPOSE 80

# assumes the server is running behind a reverse proxy (Nginx, AWS ALB, etc.)
# set the `WEB_CONCURRENCY` environment variable to the number of workers you'd like to run
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-", "--forwarded-allow-ips", "*"]
