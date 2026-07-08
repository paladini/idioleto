from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from idioleto.cli import app
from idioleto.contracts import IdiolectProfile
from idioleto.generate.ollama_client import OllamaClient
from idioleto.generate.service import generate_text

FIXTURE = Path(__file__).parent / "fixtures" / "sample.idiolect"


class FakeAdapter:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def generate(self, *, model: str, system_prompt: str, user_prompt: str) -> str:
        self.calls.append(
            {
                "model": model,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
            }
        )
        return "Generated locally."


def test_generate_text_uses_compiled_prompt_and_adapter() -> None:
    profile = IdiolectProfile.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    adapter = FakeAdapter()

    result = generate_text(
        profile,
        prompt="Write about local tools.",
        model="llama3",
        adapter=adapter,
    )

    assert result == "Generated locally."
    assert adapter.calls[0]["model"] == "llama3"
    assert "Style profile:" in adapter.calls[0]["system_prompt"]
    assert adapter.calls[0]["user_prompt"] == "Write about local tools."


def test_ollama_client_sends_expected_payload(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    captured: dict[str, object] = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, str]:
            return {"response": "hello"}

    def fake_post(url: str, *, json: dict[str, object], timeout: float) -> FakeResponse:
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("httpx.post", fake_post)

    result = OllamaClient(base_url="http://localhost:11434").generate(
        model="llama3",
        system_prompt="system",
        user_prompt="user",
    )

    assert result == "hello"
    assert captured["url"] == "http://localhost:11434/api/generate"
    assert captured["json"] == {
        "model": "llama3",
        "prompt": "user",
        "system": "system",
        "stream": False,
    }


def test_generate_cli_writes_output_file(
    tmp_path: Path, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    output = tmp_path / "draft.txt"

    monkeypatch.setattr(
        "idioleto.cli.generate_text",
        lambda *args, **kwargs: "CLI text",
    )

    result = CliRunner().invoke(
        app,
        [
            "generate",
            "--profile",
            str(FIXTURE),
            "--prompt",
            "Write.",
            "--model",
            "llama3",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert output.read_text(encoding="utf-8") == "CLI text"
    assert "Wrote" in result.output
