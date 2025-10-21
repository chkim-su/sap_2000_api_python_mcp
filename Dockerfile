FROM python:3.11-slim

WORKDIR /app

# System deps (if any). Keeping minimal.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy only metadata first for better layer caching
COPY pyproject.toml README.md MANIFEST.in ./
COPY src ./src

# Install package with stdio extras
RUN pip install --no-cache-dir .[mcp]

# Runtime env
ENV MCP_TRANSPORT=streamable-http \
    WORK_DIR=/data/work

RUN mkdir -p "$WORK_DIR"

# Start the MCP server (streamable-http for Smithery)
CMD ["python", "-m", "sap2000_mcp.stdio_server"]

