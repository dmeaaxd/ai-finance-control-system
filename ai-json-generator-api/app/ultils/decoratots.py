from datetime import datetime

from app.dto.requests import MessageRequest
from app.dto.responses import BasicResponse


def detail_def(func):
    async def wrapper(request: MessageRequest):
        start_time = datetime.now()
        result = await func(request)
        end_time = datetime.now()

        return BasicResponse(result=result.dict(), total=(end_time - start_time).total_seconds())

    return wrapper
