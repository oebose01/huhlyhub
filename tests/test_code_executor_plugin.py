from pathlib import Path
from core.plugin_loader import PluginLoader
from core import CORE_API_VERSION
from plugins.code_executor.tools import execute_python


def test_code_executor_plugin_loads():
    plugin_dir = Path("plugins/code_executor")
    loader = PluginLoader(plugin_dir)
    plugins = loader.load_all()
    assert "code_executor" in plugins
    plugin = plugins["code_executor"]
    assert plugin.core_api_version == CORE_API_VERSION
    assert len(plugin.tools) >= 1


def test_execute_simple_code():
    code = "result = 2 + 2"
    output = execute_python(code, timeout=1)
    assert output["success"] is True
    assert output["stdout"] == ""
    assert output["stderr"] == ""
    assert "result" in output["variables"]
    assert output["variables"]["result"] == 4


def test_execute_with_print():
    code = "print('hello world')"
    output = execute_python(code, timeout=1)
    assert output["success"] is True
    assert "hello world" in output["stdout"]
    assert output["stderr"] == ""


def test_execute_syntax_error():
    code = "print('hello'"
    output = execute_python(code, timeout=1)
    assert output["success"] is False
    assert "SyntaxError" in output["stderr"]


def test_execute_timeout():
    code = "import time; time.sleep(5)"
    output = execute_python(code, timeout=1)
    assert output["success"] is False
    assert "Timeout" in output["stderr"]


def test_restricted_imports():
    code = "import os; os.system('echo hacked')"
    output = execute_python(code, timeout=1)
    assert output["success"] is False
    assert "not allowed" in output["stderr"].lower()
