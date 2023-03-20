from qdrant_client import QdrantClient

from markdown_search.config import QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
from markdown_search.encode import ENCODER_MODEL
from markdown_search.encoder import OpenAIEncoder

if __name__ == '__main__':
    query = "How to enable on-disk quantization?"

    encoder = OpenAIEncoder(ENCODER_MODEL)
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)

    search_result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=encoder.encode(query),
        limit=5,
    )

    for hit in search_result:
        print(hit.payload['context'])
        print("------")
