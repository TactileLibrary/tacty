FROM mcr.microsoft.com/devcontainers/python:3.12

# Install only core system dependencies required for native Wayland GUI rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libegl1 \
    libdbus-1-3 \
    libglib2.0-0 \
    libxkbcommon0 \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy uv directly from the official OCI artifact
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/