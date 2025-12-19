from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
from parser import parse_tag_line
from db import get_last_state, upsert_state

app = FastAPI(title="BACKEND RTLS ORBRO")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("tag_logger")

class TagRequest(BaseModel):
    raw_line: str

@app.post("/tag")
async def tag(req: TagRequest):
    try:
        tag = parse_tag_line(req.raw_line)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    last_state = get_last_state(tag.tag_id)

    if last_state and last_state.cnt != tag.cnt:
        logger.info(
            f"TAG {tag.tag_id} | CNT changed: {last_state.cnt} -> {tag.cnt}"
        )

    upsert_state(tag)

    return {
        "status": "ok",
        "tag_id": tag.tag_id,
        "cnt": tag.cnt,
        "timestamp": tag.timestamp,
    }
