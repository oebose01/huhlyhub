import pytest
import tempfile
from pathlib import Path
from core.plugin_loader import PluginLoader
from core import CORE_API_VERSION
from plugins.file_io.tools import read_file, write_file


def test_file_io_plugin_loads():
    """Ensure the file_io plugin can be loaded and provides tools."""
    plugin_dir = Path("plugins/file_io")
    loader = PluginLoader(plugin_dir)
    plugins = loader.load_all()
    assert "file_io" in plugins
    plugin = plugins["file_io"]
    assert plugin.core_api_version == CORE_API_VERSION
    assert len(plugin.tools) >= 2


def test_read_file_tool():
    """Test reading a file using the read function."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("hello world")
        result = read_file("test.txt", tmpdir)
        assert result == "hello world"


def test_write_file_tool():
    """Test writing a file using the write function."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = write_file("output.txt", "new content", tmpdir)
        assert result == "success"
        assert (Path(tmpdir) / "output.txt").read_text() == "new content"


def test_path_traversal_prevention():
    """Ensure that attempts to escape the base directory are blocked."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError, match="Path traversal attempt"):
            read_file("../outside.txt", tmpdir)
        with pytest.raises(ValueError, match="Path traversal attempt"):
            write_file("../../../etc/passwd", "hack", tmpdir)
