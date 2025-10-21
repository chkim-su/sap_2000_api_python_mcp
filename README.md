# SAP2000 MCP (stdio/streamable-http)

경량 MCP 서버로, 포트 없이 stdio 또는 streamable-http(원격)로 동작합니다. CHM/DLL 없이 패키지된 SQLite DB를 사용합니다.

## 빠른 시작
- 설치: `pip install sap2000-python-api[mcp]`
- 로컬 실행(stdio): `sap2000-mcp-py` 또는 `python -m sap2000_mcp.stdio_server`

## Claude 등록
- Smithery(권장):
  ```bash
  npx @smithery/cli install sap2000-python-api --client claude
  ```
- 로컬 stdio:
  ```bash
  claude mcp add --transport stdio sap2000 sap2000-mcp-py
  ```

## 제공 도구
- `find_functions(q, top_k=10, verb_intent, expand_level, domain_hints, explain)`
- `to_python(function_id, binding_mode="direct")`

## 요구 사항
- Python >= 3.10
- 데이터베이스: 패키지 포함 `sap2000_mcp/data/sap2000_mcp.db`

## 환경 변수
- `WORK_DIR`: 작업 디렉터리(기본: `build`)
- `MCP_TRANSPORT`: `stdio`(기본) 또는 `streamable-http`