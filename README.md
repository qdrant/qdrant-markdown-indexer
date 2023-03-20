# Index markdown files into Qdrant using OpenAI embeddings

## Setup

Create `.env` file with credentials:

```bash
QDRANT_HOST=xxxxxxxxxxxx.us-east.aws.cloud.qdrant.io
QDRANT_API_KEY=......
OPENAI_API_KEY=....
```

Install dependencies:

```bash
poetry install
```

## Run

```bash
python -m markdown_search.index --docs-dir '/path/to/docs' --url-prefix 'https://example.com/docs'
```