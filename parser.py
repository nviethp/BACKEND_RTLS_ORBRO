from dataclasses import dataclass


@dataclass
class TagData:
    tag_id: str
    cnt: int
    timestamp: str

@dataclass
class TagInfo:
    id: str
    description: str


def parse_tag_line(line: str) -> TagData:
    """
    Parse format: TAG,<tag_id>,<cnt>,<timestamp>
    """
    parts = line.strip().split(",")

    if len(parts) != 4 or parts[0] != "TAG":
        raise ValueError("Invalid TAG format")

    return TagData(
        tag_id=parts[1],
        cnt=int(parts[2]),
        timestamp=parts[3],
    )
