
# openai의 chat completion api를 활용하여
# terminal 기반의 챗봇을 만들어보세요.

# 1. 내가 뭔갈 입력한다.
# 2. ai가 뭔갈 답한다.
# 1~2가 무한히 반복된다.
    # 멈추는 조건이 필요하다 - 입력을 컨트롤해서 처리할 예정입니다.

from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
model = "gpt-4o-mini"
client = OpenAI(api_key=OPENAI_API_KEY)

history = []

print('챗봇 시작')
while True:
    user_input = input('나: \n')

    if user_input == 'q':
        print('챗봇 종료')
        break
    
    if len(history) > 4:
        history = history[len(history)-4:]

    print('---------------------------')
    print(history)
    print('---------------------------')
    history.append({'role': 'user', 'content' : user_input})
    

    response = client.chat.completions.create(
        model=model,
        messages=history
    )

    assistant_response = response.choices[0].message.content
    history.append({'role': 'assistant', 'content' : assistant_response})
    print('어이스턴트 : \n', assistant_response)
    print()