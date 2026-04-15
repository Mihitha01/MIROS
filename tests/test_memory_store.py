from pathlib import Path

from miros.core.models import CommandResult, Intent, IntentCategory
from miros.memory.store import MemoryStore


def test_memory_store_persists_and_reads_interactions(tmp_path: Path) -> None:
    store = MemoryStore(db_path=tmp_path / "memory.db")

    intent = Intent(
        category=IntentCategory.CONVERSATION,
        action="chat",
        raw_text="hello",
    )
    result = CommandResult(success=True, message="hello back")

    store.record_interaction(
        user_text="hello",
        assistant_text="hello back",
        intent=intent,
        result=result,
    )

    interactions = store.get_recent_interactions(limit=5)

    assert len(interactions) == 1
    assert interactions[0]["user_text"] == "hello"
    assert interactions[0]["assistant_text"] == "hello back"
