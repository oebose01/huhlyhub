from core.interfaces import Tool, Plugin
from core import CORE_API_VERSION

tool = Tool(
    name="execute_python",
    description="Execute Python code in a sandboxed environment",
    input_schema={
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code to execute"},
            "timeout": {
                "type": "number",
                "description": "Maximum execution time in seconds",
                "default": 5,
            },
        },
        "required": ["code"],
    },
    output_schema={
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "stdout": {"type": "string"},
            "stderr": {"type": "string"},
            "variables": {"type": "object"},
        },
    },
)

plugin = Plugin(
    name="code_executor",
    version="0.1.0",
    core_api_version=CORE_API_VERSION,
    agents=[],
    tools=[tool],
)
