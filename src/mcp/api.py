from __future__ import annotations

from typing import Dict, Optional

try:
    from fastapi import FastAPI, HTTPException
except Exception:  # FastAPI optional for non-HTTP runtimes
    class HTTPException(Exception):  # type: ignore
        def __init__(self, status_code: int = 500, detail: Optional[str] = None):
            super().__init__(detail or f"HTTP {status_code}")
            self.status_code = status_code
            self.detail = detail

    class _LiteApp:  # minimal decorator-compatible stub
        def __init__(self, *_, **__):
            pass

        def get(self, *_args, **_kwargs):
            def deco(fn):
                return fn
            return deco

        def post(self, *_args, **_kwargs):
            def deco(fn):
                return fn
            return deco

        def on_event(self, *_args, **_kwargs):
            def deco(fn):
                return fn
            return deco

    FastAPI = _LiteApp  # type: ignore

from .core import (
    close as _close_conn,
    connect as _connect,
    find_functions as _find_functions,
    to_python as _to_python,
    render_hint as _render_hint,
    FindFunctionsRequest,
    FindFunctionsResponse,
    ToPythonRequest,
    ToPythonResponse,
    RenderHintRequest,
    RenderHintResponse,
)


app = FastAPI(title="SAP2000 MCP API")


@app.on_event("shutdown")
def _close() -> None:
    _close_conn()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/find_functions", response_model=FindFunctionsResponse)
def find_functions(req: FindFunctionsRequest) -> FindFunctionsResponse:
    _connect()
    return _find_functions(req)


@app.post("/to_python", response_model=ToPythonResponse)
def to_python(req: ToPythonRequest) -> ToPythonResponse:
    try:
        _connect()
        return _to_python(req)
    except KeyError:
        raise HTTPException(status_code=404, detail="function not found")


@app.post("/render_hint", response_model=RenderHintResponse)
def render_hint(req: RenderHintRequest) -> RenderHintResponse:
    try:
        _connect()
        return _render_hint(req)
    except KeyError:
        raise HTTPException(status_code=404, detail="function not found")

