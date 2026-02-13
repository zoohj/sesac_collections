import requests
from pprint import pprint
import os
from dotenv import load_dotenv
from openai import OpenAI
import sys
input= sys.stdin.readline

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
URL = "https://api.openai.com/v1/chat/completions"
model = "gpt-4o-mini"

client = OpenAI(api_key = OPENAI_API_KEY)


history = [
    {"role":"system","content":"당신은 사용자의 질문과 답변을 기억하는 비서입니다."}
]


def chat_with_memory(user_input):
    global history
    try:
        # 1. 사용자 질문을 기록에 추가
        history.append({"role": "user", "content": user_input})
        
        # 2. 전체 기록을 API에 전송
        response = client.chat.completions.create(
            model=model,
            messages=history
        )
        
        # 3. 모델의 답변을 기록에 추가 (이것이 맥락 유지의 핵심)
        answer = response.choices[0].message.content
        history.append({"role": "assistant", "content": answer})

        # 최근 10개의 대화만 유지 (시스템 메시지는 제외하고 관리하는 로직 필요)
        if len(history) > 11:  # 시스템 메시지 1개 + 대화 10개
            history = [history[0]] + history[-10:]
        
        return answer
    except Exception as e:
        return f"에러 발생: {e}"


# 실습 테스트
print("Q1: 내 이름은 jun이야.")
print(f"A1: {chat_with_memory('내 이름은 jun이야')}\n")

print("Q2: 내 이름이 뭐라고?")
print(f"A2: {chat_with_memory('내 이름이 뭐라고?')}")


while True:
    question = input().strip()
    if question == '0':
        print("답변을 종료합니다")
        break
    print(f"Answer: {chat_with_memory(question)}\n") 