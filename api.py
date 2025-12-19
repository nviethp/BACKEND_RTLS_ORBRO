from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
from parser import parse_tag_line
from db import get_last_state, upsert_state, register_tag, is_tag_registered, get_tag, get_all_tags

app = FastAPI(title="BACKEND RTLS ORBRO")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("tag_logger")

class TagRequest(BaseModel):
    raw_line: str

class RegisterTagRequest(BaseModel):
    id: str
    description: str

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

@app.get("/health")
async def health_check():
    """
    Kiểm tra trạng thái hệ thống
    """
    return {"status": "ok"}

@app.post("/tags")
async def register_tag_api(req: RegisterTagRequest):
    """
    Đăng ký Tag (id, description)
    """
    if is_tag_registered(req.id):
        raise HTTPException(status_code=400, detail="Tag already registered")

    register_tag(req.id, req.description)

    return {
        "status": "registered",
        "id": req.id,
        "description": req.description,
    }

@app.get("/tags")
async def list_tags():
    """
    Lấy danh sách Tag đã đăng ký và tra cứu trạng thái
    """
    result = []

    for tag in get_all_tags():
        state = get_last_state(tag.id)

        result.append({
            "id": tag.id,
            "description": tag.description,
            "last_cnt": state.cnt if state else None,
            "last_seen": state.timestamp if state else None,
        })

    return result


@app.get("/tag/{tag_id}")
async def get_single_tag(tag_id: str):
    """
    Tra cứu trạng thái của một Tag (single Tag)
    """
    tag = get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    state = get_last_state(tag_id)

    return {
        "id": tag.id,
        "description": tag.description,
        "last_cnt": state.cnt if state else None,
        "last_seen": state.timestamp if state else None,
    }

