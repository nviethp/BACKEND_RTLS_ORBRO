import asyncio
import httpx
from datetime import datetime

API_URL = "http://localhost:8000/tag"

TAGS = {
    "fa451f0755d8": 12,
    "bb231f09aa21": 123,
    "cc9981ffab77": 1234,
}


def build_tag_line(tag_id: str, cnt: int) -> str:
    """
    Build TAG string with format:
    TAG,<tag_id>,<cnt>,<timestamp>
    """
    ts = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]
    return f"TAG,{tag_id},{cnt},{ts}"


async def run_simulator():
    async with httpx.AsyncClient() as client:
        while True:
            for tag_id in TAGS:
                TAGS[tag_id] += 1

                line = build_tag_line(tag_id, TAGS[tag_id])

                response = await client.post(
                    API_URL,
                    json={"raw_line": line}
                )

                print(
                    f"Sent: {line} | "
                    f"Status: {response.status_code}"
                )

            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run_simulator())
