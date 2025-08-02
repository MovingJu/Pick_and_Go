FROM python:3.10-slim

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first (for cache efficiency)
COPY pyproject.toml uv.lock ./

# Install dependencies (excluding the local project itself)
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache \
    uv sync --frozen --no-install-project

# Copy full project (after deps installed for layer caching)
COPY . .

# Install local project (if needed, like if it's a package)
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache \
    uv sync --frozen

# Railway exposes PORT as env var, so use that
ENV PORT=8000

# Run the app with uvicorn via uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
