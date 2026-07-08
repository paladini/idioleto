from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from idioleto.compile import compile_profile
from idioleto.contracts import IdiolectProfile
from idioleto.generate import OllamaClient, generate_text

app = typer.Typer(
    name="idioleto",
    help="Compile local authorial style profiles and use them with local LLMs.",
    no_args_is_help=True,
)


@app.command()
def compile(
    input: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Folder containing Markdown, text, or PDF files.",
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            dir_okay=False,
            writable=True,
            help="Destination .idiolect file.",
        ),
    ],
    language: Annotated[
        str,
        typer.Option(
            "--language",
            help="Profile language tag. Use auto, en, or pt-BR.",
        ),
    ] = "auto",
) -> None:
    """Compile a folder of writing into a validated .idiolect profile."""
    try:
        profile = compile_profile(input, language=language)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            profile.model_dump_json(indent=2),
            encoding="utf-8",
        )
    except (FileNotFoundError, NotADirectoryError, ValueError, ValidationError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Wrote {output}")


@app.command()
def generate(
    profile: Annotated[
        Path,
        typer.Option(
            "--profile",
            "-p",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to a .idiolect profile.",
        ),
    ],
    prompt: Annotated[
        str,
        typer.Option("--prompt", help="Generation instruction or topic."),
    ],
    model: Annotated[
        str,
        typer.Option("--model", "-m", help="Local Ollama model name."),
    ],
    ollama_url: Annotated[
        str,
        typer.Option("--ollama-url", help="Ollama base URL."),
    ] = "http://localhost:11434",
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            dir_okay=False,
            writable=True,
            help="Optional output file. Defaults to stdout.",
        ),
    ] = None,
) -> None:
    """Generate text from a .idiolect profile through Ollama."""
    try:
        idiolect = IdiolectProfile.model_validate_json(
            profile.read_text(encoding="utf-8")
        )
        text = generate_text(
            idiolect,
            prompt=prompt,
            model=model,
            adapter=OllamaClient(base_url=ollama_url),
        )
    except (OSError, ValidationError, RuntimeError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        typer.echo(f"Wrote {output}")
    else:
        typer.echo(text)
