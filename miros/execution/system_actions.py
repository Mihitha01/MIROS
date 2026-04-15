"""System-level actions with guardrails around workspace file operations."""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path
from typing import Any


class SystemActionExecutor:
    """Executes local OS and filesystem operations."""

    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root.resolve()

    def open_app(self, app: str) -> dict[str, Any]:
        """Open a desktop application using OS-specific mechanisms."""
        system_name = platform.system().lower()
        command = app.strip()

        if system_name == "windows":
            subprocess.Popen(["cmd", "/c", "start", "", command])
        elif system_name == "darwin":
            subprocess.Popen(["open", "-a", command])
        else:
            subprocess.Popen([command])

        return {"app": app, "status": "launched"}

    def list_files(self, path: str | None = None, limit: int = 200) -> dict[str, Any]:
        """List files inside workspace (or a workspace-relative directory)."""
        target = self._resolve_workspace_path(path or ".")
        entries: list[dict[str, Any]] = []
        for index, entry in enumerate(sorted(os.scandir(target), key=lambda e: e.name)):
            if index >= limit:
                break
            entries.append(
                {
                    "name": entry.name,
                    "type": "dir" if entry.is_dir() else "file",
                    "size": entry.stat().st_size,
                }
            )

        return {"path": str(target), "entries": entries}

    def read_file(self, path: str, max_chars: int = 4000) -> dict[str, Any]:
        """Read a file in the workspace with a response size cap."""
        target = self._resolve_workspace_path(path)
        content = target.read_text(encoding="utf-8")
        truncated = len(content) > max_chars
        if truncated:
            content = content[:max_chars]
        return {
            "path": str(target),
            "content": content,
            "truncated": truncated,
        }

    def create_file(
        self,
        path: str,
        content: str,
        overwrite: bool = False,
    ) -> dict[str, Any]:
        """Create a UTF-8 file in the workspace."""
        target = self._resolve_workspace_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {target}")

        target.write_text(content, encoding="utf-8")
        return {"path": str(target), "bytes_written": len(content.encode("utf-8"))}

    def _resolve_workspace_path(self, path: str) -> Path:
        candidate = Path(path).expanduser()
        if not candidate.is_absolute():
            candidate = self.workspace_root / candidate

        resolved = candidate.resolve()
        if resolved != self.workspace_root and self.workspace_root not in resolved.parents:
            raise PermissionError("Path escapes workspace boundary.")

        return resolved
