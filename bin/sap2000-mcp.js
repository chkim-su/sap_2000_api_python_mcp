#!/usr/bin/env node
/* eslint-disable no-console */
const { spawnSync } = require('child_process');
const { resolve } = require('path');
const { existsSync } = require('fs');

function findPython() {
  const cwd = process.cwd();
  const venvWin = resolve(cwd, '.venv', 'Scripts', 'python.exe');
  const venvNix = resolve(cwd, '.venv', 'bin', 'python');
  if (existsSync(venvWin)) return venvWin;
  if (existsSync(venvNix)) return venvNix;
  return 'python';
}

function run(cmd, args, opts = {}) {
  const res = spawnSync(cmd, args, { stdio: 'inherit', shell: false, ...opts });
  if (res.error) {
    console.error(`[sap2000-mcp] Failed: ${cmd} ${args.join(' ')}`);
    console.error(res.error);
    process.exit(res.status || 1);
  }
  if (res.status !== 0) {
    process.exit(res.status);
  }
}

function inRepo() {
  return existsSync(resolve(process.cwd(), 'pyproject.toml')) || existsSync(resolve(process.cwd(), 'src', 'mcp', 'api.py'));
}

function ensureDeps(python) {
  // Try import mcp.api
  const probe = spawnSync(python, ['-c', 'import mcp.api; print("ok")']);
  if (probe.status === 0) return;
  if (inRepo()) {
    console.log('[sap2000-mcp] Installing Python package from current repo (editable) ...');
    // Include stdio extra to ensure fastmcp is available
    run(python, ['-m', 'pip', 'install', '-e', '.[mcp]']);
  } else {
    console.log('[sap2000-mcp] Installing Python package from PyPI ...');
    // Match the actual project name in pyproject.toml and include stdio extra
    run(python, ['-m', 'pip', 'install', 'sap2000-python-api[mcp]']);
  }
}

// Packaged DB is embedded in the wheel; no autobuild at runtime.
function ensureDb() { /* no-op */ }

function main() {
  const args = process.argv.slice(2);

  const python = findPython();
  ensureDeps(python);
  ensureDb();

  console.log('[sap2000-mcp] Starting stdio MCP server ...');
  run(python, ['-m', 'mcp.stdio_server']);
}

main();
