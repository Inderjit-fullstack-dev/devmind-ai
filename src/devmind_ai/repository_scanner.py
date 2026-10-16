from dataclasses import dataclass
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".py", ".cs", ".ts", ".tsx", ".js", ".jsx",
    ".java", ".go", ".rs", ".md", ".json", ".yaml", ".yml",
}

EXCLUDED_DIRECTORIES = {
    ".git", ".venv", "node_modules", "__pycache__",
    "dist", "build",
}

LANGUAGES = {
    ".py": "Python",
    ".cs": "C#",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".md": "Markdown",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".php": "PHP"
}


@dataclass(frozen=True)
class SourceFileMetadata:
    path: str
    language: str
    size_bytes: int


def scan_repository(root: Path) -> list[SourceFileMetadata]:
    root = root.resolve()

    if not root.is_dir():
        raise ValueError(f"Repository root is not a directory: {root}")

    discovered_files: list[SourceFileMetadata] = []

    for current_dir, directories, filenames in __import__("os").walk(root):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory not in EXCLUDED_DIRECTORIES
        )

        for filename in sorted(filenames):
            file_path = Path(current_dir) / filename

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:
                if file_path.is_symlink() or not file_path.is_file():
                    continue

                size_bytes = file_path.stat().st_size
            except OSError:
                continue

            discovered_files.append(
                SourceFileMetadata(
                    path=file_path.relative_to(root).as_posix(),
                    language=LANGUAGES.get(file_path.suffix.lower(), "Unknown"),
                    size_bytes=size_bytes,
                )
            )

    return sorted(discovered_files, key=lambda item: item.path)