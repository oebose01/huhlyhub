import importlib.util
import logging
from pathlib import Path
from typing import Dict, List, Optional

from core import CORE_API_VERSION
from core.interfaces import Plugin

logger = logging.getLogger(__name__)


class PluginLoadError(Exception):
    """Raised when a plugin cannot be loaded."""

    pass


class PluginLoader:
    """Loads plugins from Python files, verifying core API compatibility."""

    def __init__(self, plugin_dir: Path):
        self.plugin_dir = plugin_dir
        self._plugins: Dict[str, Plugin] = {}

    def discover_plugins(self) -> List[Path]:
        """Find the plugin.py file in the directory (if any)."""
        plugin_file = self.plugin_dir / "plugin.py"
        return [plugin_file] if plugin_file.exists() else []

    def load_plugin(self, path: Path) -> Plugin:
        """Load a single plugin file, validate version, and instantiate."""
        # Import the module
        module_name = path.stem
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Could not load spec for {path}")  # pragma: no cover
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Look for a 'plugin' variable that is a Plugin instance
        if not hasattr(module, "plugin"):
            raise PluginLoadError(f"Plugin {path} does not define a 'plugin' variable")
        plugin: Plugin = module.plugin
        if not isinstance(plugin, Plugin):
            raise PluginLoadError(f"'plugin' in {path} is not a Plugin instance")

        # Version check
        if plugin.core_api_version != CORE_API_VERSION:
            raise PluginLoadError(
                f"Plugin {plugin.name} v{plugin.version} requires core API "
                f"{plugin.core_api_version}, but current core is {CORE_API_VERSION}"
            )

        # Store
        self._plugins[plugin.name] = plugin
        logger.info(f"Loaded plugin: {plugin.name} v{plugin.version}")
        return plugin

    def load_all(self) -> Dict[str, Plugin]:
        """Discover and load all plugins in the plugin directory."""
        for path in self.discover_plugins():
            try:
                self.load_plugin(path)
            except Exception as e:
                logger.error(f"Failed to load {path}: {e}")
        return self._plugins

    def get_plugin(self, name: str) -> Optional[Plugin]:
        return self._plugins.get(name)
