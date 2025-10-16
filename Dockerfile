# Dockerfile for SAP2000 MCP Server on Smithery
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY MANIFEST.in ./
COPY README.md ./
COPY src/ ./src/
COPY bin/ ./bin/
COPY package.json ./
COPY smithery.yaml ./

# Install Python dependencies
# Install with [mcp] extra for FastMCP support
RUN pip install --no-cache-dir -e ".[mcp]"

# Expose environment variables (will be set by Smithery)
ENV MCP_TRANSPORT=streamable-http
ENV WORK_DIR=build
ENV PYTHONUNBUFFERED=1

# Healthcheck to ensure server is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Run the MCP server
CMD ["python", "-m", "mcp.stdio_server"]
