# ============================================================
# FinOps-SRE Sentinel — Tool Registry
# ============================================================
# Generated based: [Arch_Section_03], [URD_Section_03]
# Target Path: src/mcp-server/app/tool_registry.py
# ============================================================

from __future__ import annotations

import importlib
import pkgutil
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class Tool:
    """Base representation of a registered MCP tool."""

    def __init__(self, name: str, description: str, handler: Any) -> None:
        self.name = name
        self.description = description
        self.handler = handler

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        return await self.handler(input_data)


class ToolRegistry:
    """Discovers, registers, and dispatches MCP tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._auto_discover()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, name: str, description: str, handler: Any) -> None:
        """Register a single tool."""
        self._tools[name] = Tool(name=name, description=description, handler=handler)
        logger.info("tool_registered", tool=name)

    def get_tool(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {"name": t.name, "description": t.description}
            for t in self._tools.values()
        ]

    # ------------------------------------------------------------------
    # Auto-discovery
    # ------------------------------------------------------------------

    def _auto_discover(self) -> None:
        """Import every module in app.tools and register tools it exposes."""
        import app.tools as tools_pkg  # noqa: PLC0415

        for _importer, mod_name, _is_pkg in pkgutil.iter_modules(tools_pkg.__path__):
            module = importlib.import_module(f"app.tools.{mod_name}")
            handler = getattr(module, "execute", None)
            description = getattr(module, "DESCRIPTION", mod_name)
            if handler is not None:
                self.register(name=mod_name, description=description, handler=handler)