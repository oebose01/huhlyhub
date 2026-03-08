from pathlib import Path


def read_file(path: str, base_dir: str) -> str:
    """Read file safely within base_dir."""
    full_path = Path(base_dir) / path
    # Security: ensure path is within base_dir
    if not str(full_path.resolve()).startswith(str(Path(base_dir).resolve())):
        raise ValueError("Path traversal attempt")
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return full_path.read_text()


def write_file(path: str, content: str, base_dir: str) -> str:
    """Write file safely within base_dir."""
    full_path = Path(base_dir) / path
    if not str(full_path.resolve()).startswith(str(Path(base_dir).resolve())):
        raise ValueError("Path traversal attempt")
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content)
    return "success"
