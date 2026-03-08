from core.interfaces import Tool, Plugin
from core import CORE_API_VERSION

read_tool = Tool(
    name="read_file",
    description="Read a file from the allowed directory",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative path within base directory",
            },
            "base_dir": {
                "type": "string",
                "description": "Base directory (sandbox root)",
            },
        },
        "required": ["path", "base_dir"],
    },
    output_schema={"type": "string"},
)

write_tool = Tool(
    name="write_file",
    description="Write content to a file within the allowed directory",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"},
            "base_dir": {"type": "string"},
        },
        "required": ["path", "content", "base_dir"],
    },
    output_schema={"type": "string"},
)

plugin = Plugin(
    name="file_io",
    version="0.1.0",
    core_api_version=CORE_API_VERSION,
    agents=[],
    tools=[read_tool, write_tool],
)
