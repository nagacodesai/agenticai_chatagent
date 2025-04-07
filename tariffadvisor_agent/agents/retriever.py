from pinecone import Pinecone, ServerlessSpec
from agents.env_loader import PINECONE_API_KEY, PINECONE_INDEX, PINECONE_ENV
from agents.embedder import get_embedding

print(f"🔐 Pinecone Setup: API={PINECONE_API_KEY}, Index={PINECONE_INDEX}, Env={PINECONE_ENV}")

# ✅ Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# ✅ Auto-create index if missing
if PINECONE_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
    )
    print(f"✅ Created Pinecone index: {PINECONE_INDEX}")

# ✅ Load index
index = pc.Index(PINECONE_INDEX)

class RetrieverAgent:
    def retrieve_context(self, query, top_k=5):
        vector = get_embedding(query)
        result = index.query(vector=vector, top_k=top_k, include_metadata=True)
        return [match['metadata']['text'] for match in result['matches']]
