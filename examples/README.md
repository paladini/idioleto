# Examples

This directory contains a small sample corpus and a sample `.idiolect` profile.

Compile the sample corpus:

```bash
python -m idioleto compile --input examples/corpus --output examples/sample.idiolect
```

Generate text with Ollama:

```bash
python -m idioleto generate \
  --profile examples/sample.idiolect \
  --prompt "Write a short note about local-first AI tools." \
  --model llama3
```

The generation command requires Ollama to be running locally with the selected
model available.
