import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
from urllib.parse import urljoin

import mistletoe
from mistletoe import HTMLRenderer

from markdown_search.config import DATA_DIR

HEADER_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']


@dataclass
class PageAbstract:
    title: str
    text: str
    context: str
    url: str
    file: str
    sections: Optional[List[str]] = None


class MarkdownParser:
    """
    Class which converts a directory of markdown files into a list of abstracts, suitable for indexing.
    """

    def __init__(self, directory: Path, url_prefix: str, text_size=3, context_size: int = 5):
        """

        :param directory: directory containing markdown files
        :param url_prefix:  prefix to add to the url of each page. Example `{url_prefix}/{file_name}#{section}`
        :param text_size: how many sentences to group together as a text to search
        :param context_size: how many sentences to group together as a context, 0 means no context
        """
        self.directory = directory
        self.url_prefix = url_prefix
        self.context_size = context_size
        self.text_size = text_size

    def read_files(self):
        for file in self.directory.glob('*.md'):
            with open(file, 'r') as f:
                yield file, f.read()

    @classmethod
    def convert_header_to_url(cls, header: str) -> str:
        # Remove non-alphanumeric characters
        header = re.sub(r'[^a-zA-Z0-9 ]', '', header).strip()
        return header.lower().replace(' ', '-')

    def parse_file(self, file_name: Path, text):
        doc_html = mistletoe.markdown(text, renderer=HTMLRenderer)

        # file name without extension
        section_name = file_name.stem

        file_name = file_name.relative_to(self.directory)

        current_header = ""
        texts = []
        context = []
        headers_stack = [(section_name, 0)]
        code = None

        for line in text.splitlines():

            if line.startswith('```'):
                if code:
                    line = code
                    code = None
                else:
                    code = line
                    continue

            if code:
                code = code + "\n" + line
                continue

            if line.startswith('#'):
                current_header = line
                current_level = len(line) - len(line.lstrip('#'))
                # Remove header from stack if it has higher level
                while headers_stack and headers_stack[-1][1] >= current_level:
                    headers_stack.pop()
                headers_stack.append((current_header, current_level))

            if not line:
                continue

            texts.append(line)
            context.append(line)
            if len(context) > self.context_size:
                context.pop(0)

            if len(texts) > self.text_size:
                texts.pop(0)

            url = urljoin(self.url_prefix, section_name)
            headers = [section[0] for section in headers_stack]

            yield PageAbstract(
                title=current_header,
                text='\n'.join(headers + texts),
                context='\n'.join(headers + context),
                url=f'{url}#{self.convert_header_to_url(current_header)}',
                file=str(file_name),
                sections=headers
            )

        url = urljoin(self.url_prefix, section_name)
        headers = [section[0] for section in headers_stack]

        yield PageAbstract(
            title=section_name,
            text='\n'.join(headers + context),
            context='\n'.join(headers + context),
            url=f'{url}#{self.convert_header_to_url(section_name)}',
            file=str(file_name),
            sections=headers
        )


if __name__ == '__main__':
    directory = Path('/home/generall/projects/vector_search/docs/qdrant/v1.1.x')
    parser = MarkdownParser(directory, 'https://qdrant.tech/documentation/')

    output_path = Path(DATA_DIR) / 'docs.jsonl'

    with open(output_path, 'w') as f:
        for file, text in parser.read_files():
            for abstract in parser.parse_file(file, text):
                f.write(json.dumps(abstract.__dict__))
                f.write('\n')

