FROM python:3.13-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1


COPY pyproject.toml uv.lock ./


RUN uv sync 


COPY main.py ./main.py
COPY  backend ./backend
COPY  frontend ./frontend
COPY  README.md ./README.md


RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "--frozen", "uvicorn", "backend.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]