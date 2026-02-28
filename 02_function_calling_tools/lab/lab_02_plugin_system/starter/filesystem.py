"""
ListFilesTool — A Secure Filesystem Tool
==========================================
Lists files in a directory, but ONLY if:
  1. The user has "filesystem:read" permission (enforced by ToolRegistry)
  2. The path passes sanitization (no directory traversal)

The name, description, permissions, and parameters are already implemented.
Your task: implement execute().
"""

import os
from typing import Dict, Any
from base import BaseTool
from security import PathSanitizer, SecurityError


class ListFilesTool(BaseTool):
    """Lists files in a directory with security controls."""

    BASE_DIR = "."

    @property
    def name(self) -> str:
        return "list_files"

    @property
    def description(self) -> str:
        return "Lists files in a specific directory. Requires filesystem:read permission."

    @property
    def permissions(self) -> list[str]:
        return ["filesystem:read"]

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list files from."
                }
            },
            "required": ["path"]
        }

    def execute(self, path: str = ".", **kwargs) -> Dict[str, Any]:
        """
        List files in the given directory.

        Steps:
          1. Validate the path using PathSanitizer.validate_safe_path(self.BASE_DIR, path)
          2. List directory contents with os.listdir(safe_path)
          3. Return {"success": True, "result": [filenames], "error": None}
             or on error: {"success": False, "result": None, "error": "..."}

        Catch SecurityError and generic Exception separately.
        """
        # TODO: Implement execute()
        pass


if __name__ == "__main__":
    tool = ListFilesTool()
    print(f"Name:        {tool.name}")
    print(f"Permissions: {tool.permissions}")
    print(f"\nList '.':    {tool.execute(path='.')}")
    print(f"\nAttack '../../': {tool.execute(path='../../')}")
