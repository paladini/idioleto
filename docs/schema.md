# `.idiolect` schema

The `.idiolect` format is a JSON profile that represents a person's authorial
style without storing the full source corpus.

The canonical schema file is
`src/idioleto/schema/idiolect.schema.json`.

## Top-level fields

- `schema_version`: The file format version. The current version is `0.1.0`.
- `profile_id`: A stable identifier for the profile.
- `created_at`: The UTC timestamp when the profile was compiled.
- `language`: The primary language tag, such as `en` or `pt-BR`.
- `source_summary`: Counts and extensions from the compiled corpus.
- `stylometrics`: Quantitative style markers.
- `semantic_anchors`: Short, high-signal snippets and optional embeddings.

## Stylometrics

The v1 compiler records:

- `average_sentence_length`: Average words per sentence.
- `type_token_ratio`: Unique tokens divided by total tokens.
- `punctuation_density`: Punctuation marks per 100 words.
- `passive_voice_ratio`: A lightweight estimate, not a full grammar parse.
- `disallowed_ngrams`: Phrases the generator should avoid.

## Semantic anchors

Semantic anchors preserve small excerpts that express worldview, memory,
philosophy, preferences, self-description, or argument patterns.

Embeddings are optional. A profile without embeddings is still valid.

If an anchor includes `embedding`, it must also include `embedding_model`.

## Privacy guidance

Do not treat `.idiolect` files as anonymous. They can contain personal writing
style and short personal snippets.

Share profiles only when you are comfortable sharing the selected anchors and
the aggregate style metadata.
