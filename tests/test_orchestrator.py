import pytest
from pathlib import Path
from core.plugin_loader import PluginLoader
from core.interfaces import Tool
from core import CORE_API_VERSION

# Create an instance of Tool instead of subclassing
echo_tool = Tool(
    name="echo",
    description="Echoes the input message",
    input_schema={"type": "object", "properties": {"message": {"type": "string"}}},
    output_schema={"type": "string"},
)


@pytest.mark.asyncio
async def test_orchestrator_plugin_loads():
    plugin_dir = Path("plugins/orchestrator")
    loader = PluginLoader(plugin_dir)
    plugins = loader.load_all()
    assert "orchestrator" in plugins
    plugin = plugins["orchestrator"]
    assert plugin.core_api_version == CORE_API_VERSION
    assert len(plugin.agents) > 0


@pytest.mark.asyncio
async def test_orchestrator_agent_executes_tool():
    plugin_dir = Path("plugins/orchestrator")
    loader = PluginLoader(plugin_dir)
    plugins = loader.load_all()
    plugin = plugins["orchestrator"]
    agent = plugin.agents[0]

    context = {"tools": [echo_tool]}
    result = await agent.run({"message": "hello"}, context)
    assert result == "hello"
