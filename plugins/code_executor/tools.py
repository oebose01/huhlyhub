import io
import traceback
import json
from contextlib import redirect_stdout, redirect_stderr
import threading
import builtins


class TimeoutException(Exception):
    pass


def execute_python(code: str, timeout: float = 5) -> dict:
    """
    Execute Python code in a restricted environment with a timeout.
    Returns dict with success, stdout, stderr, and captured variables.
    """
    # Restricted builtins: remove dangerous functions
    safe_builtins = {
        "print": builtins.print,
        "range": builtins.range,
        "len": builtins.len,
        "str": builtins.str,
        "int": builtins.int,
        "float": builtins.float,
        "list": builtins.list,
        "dict": builtins.dict,
        "tuple": builtins.tuple,
        "set": builtins.set,
        "bool": builtins.bool,
        "abs": builtins.abs,
        "min": builtins.min,
        "max": builtins.max,
        "sum": builtins.sum,
        "enumerate": builtins.enumerate,
        "zip": builtins.zip,
        "any": builtins.any,
        "all": builtins.all,
        "sorted": builtins.sorted,
        "reversed": builtins.reversed,
        "Exception": builtins.Exception,
        "ValueError": builtins.ValueError,
        "TypeError": builtins.TypeError,
        "KeyError": builtins.KeyError,
        "IndexError": builtins.IndexError,
        "AttributeError": builtins.AttributeError,
    }

    namespace = {}

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    result = {"success": False, "stdout": "", "stderr": "", "variables": {}}
    thread = None

    def target():
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Compile code
                compiled = compile(code, "<string>", "exec")
                # Execute with restricted builtins and empty namespace
                exec(compiled, {"__builtins__": safe_builtins}, namespace)
            result["success"] = True
        except Exception:
            stderr_capture.write(traceback.format_exc())
            result["success"] = False
        finally:
            result["stdout"] = stdout_capture.getvalue()
            result["stderr"] = stderr_capture.getvalue()
            # Filter namespace to only include simple types
            safe_vars = {}
            for k, v in namespace.items():
                if k.startswith("__"):
                    continue
                try:
                    # Check if JSON serializable
                    json.dumps({k: v})
                    safe_vars[k] = v
                except (TypeError, OverflowError):
                    safe_vars[k] = str(type(v))
            result["variables"] = safe_vars

    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # Timeout
        result["success"] = False
        result["stderr"] = "Timeout: execution exceeded {} seconds".format(timeout)
        # Note: thread continues running but is daemon, will be killed when main exits.
        # In a real server, we'd need proper cleanup.

    return result
