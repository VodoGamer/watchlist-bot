FROM ghcr.io/astral-sh/uv:python3.14-alpine AS base
WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project

COPY ./alembic.ini /app/
COPY migrations/ /app/migrations
COPY src/ /app/src

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  --mount=type=bind,source=README.md,target=README.md \
  uv sync --locked

CMD [ "uv", "run", "watchlist-bot" ]
