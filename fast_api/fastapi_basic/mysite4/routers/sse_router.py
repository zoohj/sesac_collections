# routers/sse_router.py

import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/sse", tags=["SSE (Server-Sent Events)"])

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@router.get("/countdown")
def sse_countdown():
    def generate():
        for i in range(5, 0, -1):
            # SSE 형식: "data: 내용\\n\\n" (빈 줄이 이벤트 구분자)
            yield f"data: {i}\n\n"
            time.sleep(1)
        yield "data: 발사!\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/fake-llm")
def fake_llm_stream():
    fake_response = "안녕하세요! 저는 AI 어시스턴트입니다."
    tokens = list(fake_response)  # 한 글자씩 토큰으로 분리

    def generate():
        for token in tokens:
            yield f"data: {token}\n\n"
            time.sleep(0.05)
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


#################################
# OpenAI API 스트리밍
#################################


@router.get("/chat-normal")
def openai_chat_normal(message: str = "안녕하세요, 자기소개 해주세요."):
    """
    OpenAI API 일반 응답 (스트리밍 X)
    → 전체 응답이 한 번에 도착 (스트리밍과 비교용)
    """
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="2문장 이내로 대답해줘.",
        input=[{"role": "user", "content": message}],
    )
    return {"message": response.output_text}


@router.get("/chat")
def openai_chat(message: str = "안녕하세요, 자기소개 해주세요."):
    """
    실제 OpenAI API 스트리밍
    → GPT가 생성하는 답변이 토큰 단위로 실시간 도착
    """
    stream = client.responses.create(
        model="gpt-4o-mini",
        instructions="2문장 이내로 대답해줘.",
        input=[{"role": "user", "content": message}],
        stream=True,
    )

    def generate():
        for event in stream:
            if event.type == "response.output_text.delta":
                yield f"data: {event.delta}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
