FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY src/app.py .
COPY src/templates/ templates/
COPY src/static/ static/

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 3000

CMD ["uv", "run", "python", "app.py"]
