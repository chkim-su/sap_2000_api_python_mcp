from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EnvironmentConfig:
    """Minimal runtime configuration for packaged usage."""

    work_dir: Path

    @staticmethod
    def from_env() -> "EnvironmentConfig":
        value = os.environ.get("WORK_DIR")
        if not value:
            raise EnvironmentError("Environment variable WORK_DIR is required")
        return EnvironmentConfig(work_dir=Path(value).expanduser().resolve())


DEFAULT_ENV = EnvironmentConfig(
    work_dir=Path(os.environ.get("WORK_DIR", "build")).resolve(),
)

