import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

async def create_schema():
    conn = await asyncpg.connect(os.getenv("POSTGRES_URL"))
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            mode VARCHAR(20) DEFAULT 'relational',
            started_at TIMESTAMP DEFAULT NOW(),
            ended_at TIMESTAMP,
            summary TEXT
        );
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS memory_items (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            category VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            stability_tier VARCHAR(10) DEFAULT 'fact',
            sensitivity BOOLEAN DEFAULT FALSE,
            version INTEGER DEFAULT 1,
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS memory_proposals (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id UUID REFERENCES sessions(id),
            proposed_content TEXT NOT NULL,
            category VARCHAR(20) NOT NULL,
            confidence FLOAT,
            status VARCHAR(20) DEFAULT 'pending_review',
            reviewer_note TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            reviewed_at TIMESTAMP
        );
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            action VARCHAR(20) NOT NULL,
            target_type VARCHAR(20),
            target_id UUID,
            before_content TEXT,
            after_content TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    await conn.close()
    print("✅ Memory schema created successfully!")
    print("Tables created: sessions, memory_items, memory_proposals, audit_logs")

asyncio.run(create_schema())