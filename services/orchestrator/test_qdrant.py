from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

# Connect to Qdrant
qdrant = QdrantClient(url="http://localhost:6333")
print("✅ Connected to Qdrant!")

# Create collection
qdrant.recreate_collection(
    collection_name="lucien_memories",
    vectors_config=VectorParams(
        size=4,
        distance=Distance.COSINE
    )
)
print("✅ Collection created!")

# Store a test point with a fake vector
qdrant.upsert(
    collection_name="lucien_memories",
    points=[
        PointStruct(
            id=str(uuid.uuid4()),
            vector=[0.1, 0.2, 0.3, 0.4],
            payload={"text": "test memory", "type": "fact"}
        )
    ]
)
print("✅ Test point stored!")

# Search
results = qdrant.search(
    collection_name="lucien_memories",
    query_vector=[0.1, 0.2, 0.3, 0.4],
    limit=1
)

print(f"✅ Search result: {results[0].payload['text']}")
print("\n✨ Qdrant working!")