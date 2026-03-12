import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

async def test_memory():
    conn = await asyncpg.connect(os.getenv("POSTGRES_URL"))

    # Create a test session
    session_id = await conn.fetchval("""
        INSERT INTO sessions (mode)
        VALUES ('relational')
        RETURNING id;
    """)
    print(f"✅ Session created: {session_id}")

    # Store a test memory
    memory_id = await conn.fetchval("""
        INSERT INTO memory_items (category, content, stability_tier)
        VALUES ('fact', 'Dasia is building Project VALE — a local-first AI companion platform.', 'fact')
        RETURNING id;
    """)
    print(f"✅ Memory stored: {memory_id}")

    # Create a memory proposal
    proposal_id = await conn.fetchval("""
        INSERT INTO memory_proposals (session_id, proposed_content, category, confidence)
        VALUES ($1, 'Dasia loves dark romance and fantasy books.', 'preference', 0.95)
        RETURNING id;
    """, session_id)
    print(f"✅ Proposal created: {proposal_id}")

    # Read memories back
    print("\n📖 Reading memories back:")
    memories = await conn.fetch("SELECT category, content, stability_tier FROM memory_items;")
    for memory in memories:
        print(f"  [{memory['category']}] {memory['content']} (tier: {memory['stability_tier']})")

    # Read proposals back
    print("\n📬 Pending proposals:")
    proposals = await conn.fetch("SELECT proposed_content, confidence, status FROM memory_proposals;")
    for proposal in proposals:
        print(f"  {proposal['proposed_content']} (confidence: {proposal['confidence']}, status: {proposal['status']})")

    await conn.close()
    print("\n✨ Memory system working!")

asyncio.run(test_memory())