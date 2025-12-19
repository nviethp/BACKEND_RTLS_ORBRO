from typing import Dict, Optional
from parser import TagData

# In-memory state store
_tag_state: Dict[str, TagData] = {}


def get_last_state(tag_id: str) -> Optional[TagData]:
    """
    GET CNT + timestamp 
    """
    return _tag_state.get(tag_id)


def upsert_state(tag: TagData) -> None:
    """
    Save Tag
    """
    _tag_state[tag.tag_id] = tag
