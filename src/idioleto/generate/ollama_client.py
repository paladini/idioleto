from __future__ import annotations

import httpx


class OllamaClient:
    def __init__(
        self, base_url: str = "http://localhost:11434", timeout: float = 120.0
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, *, model: str, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": model,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
        }
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            msg = (
                "Could not generate text through Ollama. "
                f"Check that Ollama is running at {self.base_url}."
            )
            raise RuntimeError(msg) from exc

        data = response.json()
        generated = data.get("response")
        if not isinstance(generated, str):
            msg = "Ollama returned an invalid response payload."
            raise RuntimeError(msg)
        return generated
