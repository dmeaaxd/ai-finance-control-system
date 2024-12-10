from fastapi import FastAPI

from app.dto.requests import MessageRequest
from app.dto.responses import ErrorResponse, BasicResponse
from app.exceptions.openai_exceprions import OpenAIResponseError
from app.services.ai_handler import openai
from app.ultils.decoratots import detail_def

app = FastAPI()


@app.post("/operation/detail", response_model=BasicResponse, summary="Получить описание траты от OpenAI")
@detail_def
async def get_processed_transaction(request: MessageRequest) -> BasicResponse:
    try:
        return openai.get_details(request.message)

    except OpenAIResponseError as ex:
        return ErrorResponse(error=422, detail=str(ex))
