import os

from dotenv import load_dotenv

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

load_dotenv()

QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = os.environ.get("QDRANT_PORT", 6333)
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME", "qdrant-openai-docs")

# OPENAI_ORG_ID = os.environ.get("OPENAI_ORG_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if __name__ == '__main__':
    print(DATA_DIR)
