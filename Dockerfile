# Dockerfile for SAP2000 MCP Server on Smithery
FROM python:3.10-slim

WORKDIR /app

# Copy all project files
COPY . .

# Install the package with MCP dependencies
RUN pip install --no-cache-dir ".[mcp]"

# Set environment variables
ENV MCP_TRANSPORT=streamable-http
ENV PYTHONUNBUFFERED=1

# Run the MCP server
CMD ["python", "-m", "mcp.stdio_server"]
