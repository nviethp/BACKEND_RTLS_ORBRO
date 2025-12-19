from typing import Dict, Optional
from parser import TagData, TagInfo

# In-memory state store
_tag_state: Dict[str, TagData] = {}
_registered_tags: Dict[str, TagInfo] = {}

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


def register_tag(tag_id: str, description: str) -> None:
    """
    Register Tag
    """
    _registered_tags[tag_id] = TagInfo(tag_id, description)


def is_tag_registered(tag_id: str) -> bool:
    return tag_id in _registered_tags


def get_tag(tag_id: str) -> Optional[TagInfo]:
    return _registered_tags.get(tag_id)


def get_all_tags():
    return list(_registered_tags.values())
