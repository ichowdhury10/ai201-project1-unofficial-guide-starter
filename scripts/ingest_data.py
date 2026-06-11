"""
One-shot script to manually trigger ingestion of all files in the data/ directory.
The FastAPI app auto-ingests on startup, so this script is only needed if you
want to re-ingest outside of a running server (e.g., in tests or CI).

Usage:
    cd backend
    python ../scripts/ingest_data.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path so app imports work
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.services.rag_service import ingest_data_dir, list_documents


async def main():
    print("Starting ingestion of documents/ directory...")
    ingested = await ingest_data_dir()

    if ingested:
        print(f"\nIngested {len(ingested)} new documents:")
        for name in ingested:
            print(f"  - {name}")
    else:
        print("\nNo new documents to ingest (all already indexed).")

    docs = list_documents()
    print(f"\nTotal documents in index: {len(docs)}")
    for doc in docs:
        print(f"  [{doc.id}] {doc.name} — {doc.chunks} chunks")


if __name__ == "__main__":
    asyncio.run(main())
