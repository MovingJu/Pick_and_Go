FROM python:3.10-slim

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy full project after installing dependencies
ADD . /app

# Sync the project dependencies (including project package itself)
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache \
    uv sync --frozen

# Run the app using uvicorn via uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
