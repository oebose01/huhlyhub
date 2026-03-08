import pytest
import tempfile
from pathlib import Path
from core.plugin_loader import PluginLoader


@pytest.mark.asyncio
async def test_orchestrator_with_file_io():
    # Load both plugins
    orch_loader = PluginLoader(Path("plugins/orchestrator"))
    file_loader = PluginLoader(Path("plugins/file_io"))

    orch_plugin = orch_loader.load_all()["orchestrator"]
    file_plugin = file_loader.load_all()["file_io"]

    agent = orch_plugin.agents[0]
    tools = file_plugin.tools

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("hello from file")

        context = {"tools": tools}
        input_data = {
            "tool": "read_file",
            "args": {"path": "test.txt", "base_dir": tmpdir},
        }
        result = await agent.run(input_data, context)
        assert result == "hello from file"

        input_data = {
            "tool": "write_file",
            "args": {
                "path": "output.txt",
                "content": "new content",
                "base_dir": tmpdir,
            },
        }
        result = await agent.run(input_data, context)
        assert result == "success"
        assert (Path(tmpdir) / "output.txt").read_text() == "new content"
