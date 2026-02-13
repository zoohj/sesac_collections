

import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint

from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

client = OpenAI(api_key=OPENAI_API_KEY)

model = 'gpt-4o-mini'

# 1. ai한테 특정 키워드에 대한 뉴스를 물어볼겁니다.


tools = [
    {
        "type": "function",
        "name": "get_news",
        "description": "네이버 뉴스 api를 활용하여 query에 대한 뉴스 데이터를 가지고 오는 함수.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "뉴스 검색어",
                },
            },
            "required": ["query"],
        },
    },
]

def get_news(query):
    URL = "https://openapi.naver.com/v1/search/news.json"

    params = {
        'query' : query
    }

    headers = {
        'X-Naver-Client-Id' : NAVER_CLIENT_ID,
        'X-Naver-Client-Secret' : NAVER_CLIENT_SECRET
    }

    try:
        response = requests.get(URL, params=params, headers=headers)
        response.raise_for_status()

        return response.json()
    except Exception as e:
        print(e)

# pprint(get_news('openai'))

initial_prompt = '멀티캠퍼스에 대한 최신 뉴스 알려줘'
input_list = [
    {"role": "developer", "content": "너는 진실만을 말하는 뉴스 전달자야. 주어진 정보를 바탕으로 정확한 정보만 전달해줘. 고유명사, 이름, 숫자, 단위 등은 그대로 사용해."},
    {"role": "user", "content": initial_prompt}
]

response = client.responses.create(
    model=model,
    input=input_list,
    tools=tools
)

# pprint(response.output)

input_list += response.output

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_news":
            # 3. Execute the function logic for get_horoscope
            result = get_news(**json.loads(item.arguments))
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "result": result
                })
            })


response = client.responses.create(
    model=model,
    instructions="주어진 정보를 바탕으로 나에게 요약해줘.",
    tools=tools,
    input=input_list + [{'role' : 'user', 'content' : 'function_call_out에서 주어진 정보를 바탕으로 나에게 요약해줘. 주어진 정보만을 사용해서 응답해. 주어진 정보만을 사용해서 응답해.'}],
    temperature=0
)
# input_list = [
#     + 시스템 프롬프트 / developer prompt
#     1. user가 질문한 내용 [role : user]
#     2. user의 질문에 대해 ai가 함수를 실행시키라고 하는 명령 [ function_call]
#     3. 명령에 대한 실행, 즉 함수의 결과가 들어있습니다. [function_call_out]
#     +  user의 명령 : 요약해줘 [role : user]
# ]
pprint(response.output_text)