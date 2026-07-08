from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


@dataclass(frozen=True)
class LoadedDocument:
    path: Path
    text: str


def load_corpus(input_dir: Path) -> list[LoadedDocument]:
    if not input_dir.exists():
        msg = f"Input folder does not exist: {input_dir}"
        raise FileNotFoundError(msg)
    if not input_dir.is_dir():
        msg = f"Input path is not a folder: {input_dir}"
        raise NotADirectoryError(msg)

    documents: list[LoadedDocument] = []
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        text = _read_supported_file(path)
        if text.strip():
            documents.append(LoadedDocument(path=path, text=text))
    return documents


def _read_supported_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        return _read_pdf(path)
    msg = f"Unsupported file extension: {path.suffix}"
    raise ValueError(msg)


def _read_pdf(path: Path) -> str:
    try:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:  # noqa: BLE001
        msg = f"Could not read PDF file: {path}"
        raise ValueError(msg) from exc

