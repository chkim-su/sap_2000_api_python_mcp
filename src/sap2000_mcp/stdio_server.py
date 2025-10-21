from __future__ import annotations

import os
from typing import List, Optional, Dict, Any

try:
    from fastmcp import FastMCP
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "fastmcp is required for stdio transport. Install with: pip install fastmcp"
    ) from e

from .core import (
    FindFunctionsRequest,
    find_functions as _find_functions,
    ToPythonRequest,
    to_python as _to_python,
)


app = FastMCP("SAP2000 MCP")


@app.tool()
def find_functions(
    q: str,
    top_k: int = 10,
    verb_intent: Optional[str] = None,
    expand_level: Optional[str] = None,
    domain_hints: Optional[List[str]] = None,
    explain: bool = True,
) -> Dict[str, Any]:
    req = FindFunctionsRequest(
        q=q,
        top_k=top_k,
        verb_intent=verb_intent,
        expand_level=expand_level,
        domain_hints=domain_hints,
        explain=explain,
    )
    resp = _find_functions(req)
    return resp.model_dump()


@app.tool()
def to_python(function_id: int, binding_mode: str = "direct") -> Dict[str, Any]:
    req = ToPythonRequest(function_id=function_id, binding_mode=binding_mode)
    resp = _to_python(req)
    return resp.model_dump()


def main() -> None:  # pragma: no cover
    # Support both stdio (local) and streamable-http (Smithery remote hosting)
    transport_mode = os.getenv("MCP_TRANSPORT", "stdio").strip()

    if transport_mode == "streamable-http":
        # Configure CORS for browser-based clients (Smithery scanner)
        try:
            from starlette.middleware import Middleware
            from starlette.middleware.cors import CORSMiddleware
            cors = [
                Middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_methods=["*"],
                    allow_headers=["*"],
                    allow_credentials=True,
                    expose_headers=["Mcp-Session-Id"],
                )
            ]
        except Exception:
            cors = []

        host = os.getenv("HOST") or os.getenv("FASTMCP_HOST") or "0.0.0.0"
        try:
            port = int(os.getenv("PORT") or os.getenv("FASTMCP_PORT") or "8000")
        except Exception:
            port = 8000

        app.run(
            transport="streamable-http",
            host=host,
            port=port,
            middleware=cors,
        )
    else:
        # For local stdio mode (default)
        app.run(transport="stdio")


if __name__ == "__main__":  # pragma: no cover
    main()
