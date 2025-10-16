# SAP2000 MCP (stdio, no ports)

경량 stdio 기반 MCP 서버입니다. CHM/DLL 없이 내장된 SQLite DB만 사용합니다. 원격 호스팅이나 로컬 포트가 필요하지 않습니다.

## 빠른 시작
- Python 설치형
  - 설치: `pip install sap2000-python-api[mcp]`
  - 실행: `sap2000-mcp-py` 또는 `python -m mcp.stdio_server`
- Node CLI(선택)
  - 설치: `npm i -g @tntndi001/sap2000-python-api`
  - 실행: `sap2000-mcp` (필요 시에만 프로세스 실행)

## Claude 등록 예

### 방법 1: Smithery를 통한 원격 호스팅 (권장)
사용자가 설치 없이 바로 사용할 수 있습니다:
```bash
npx @smithery/cli install sap2000-python-api --client claude
```

### 방법 2: 로컬 stdio 모드
```bash
claude mcp add --transport stdio sap2000 sap2000-mcp-py
# 또는
claude mcp add --transport stdio sap2000 sap2000-mcp
```

## 제공 도구
- `find_functions(q, top_k=10, verb_intent, expand_level, domain_hints, explain)`
- `to_python(function_id, binding_mode="direct")`

## 런타임 제약
- CHM/DLL 불필요, 불포함(배포 제외)
- SQLite DB 내장: `mcp/data/sap2000_mcp.db`
- Python >= 3.10

## 배포 옵션

### Smithery 원격 호스팅
Smithery를 통해 원격 호스팅됩니다. 사용자는 포트 설정이나 로컬 설치 없이 바로 사용할 수 있습니다.
- 배포 URL: https://smithery.ai
- 설치: `pip install sap2000-python-api[smithery]`
- 환경 변수: `MCP_TRANSPORT=streamable-http`

### 로컬 설치
- Python: `pip install sap2000-python-api[mcp]`
- Node.js: `npm i -g @tntndi001/sap2000-python-api`

## 개발자 참고
- HTTP 서버는 선택적(extra: `http`): `pip install .[http]`
- Smithery 배포: `pip install .[smithery]`
- 빌드/스크립트/테스트 산출물은 배포에서 제외됩니다.
- 환경 변수:
  - `WORK_DIR`: 데이터베이스 위치 (기본값: `build`)
  - `MCP_TRANSPORT`: `stdio` (기본) 또는 `streamable-http` (Smithery)
