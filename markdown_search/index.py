import argparse
import json
from pathlib import Path

from markdown_search.config import DATA_DIR
from markdown_search.encode import upload
from markdown_search.parser import MarkdownParser

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                    prog='Qdrant Markdown Indexer',
                    description='Converts a directory of markdown files into a Qdrant collection')

    parser.add_argument('--docs-dir', type=str, required=True)
    parser.add_argument('--url-prefix', type=str, required=True)

    args = parser.parse_args()

    directory = Path(args.docs_dir)
    parser = MarkdownParser(directory, url_prefix=args.url_prefix)

    output_path = Path(DATA_DIR) / 'docs.jsonl'

    with open(output_path, 'w') as f:
        for file, text in parser.read_files():
            for abstract in parser.parse_file(file, text):
                f.write(json.dumps(abstract.__dict__))
                f.write('\n')

    upload_path = Path(DATA_DIR) / 'docs.jsonl'

    upload(upload_path)
