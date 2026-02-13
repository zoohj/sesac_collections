import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 1. 환경 설정
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

st.set_page_config(page_title="나만의 AI 비서", page_icon="🤖")
st.title("🤖 AI 대화 비서")
st.caption("무엇이든 물어보세요! (종료하려면 브라우저를 닫으세요)")

# 2. 대화 기록 초기화 (Streamlit의 상태 유지 기능)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 사용자의 질문과 답변을 기억하는 비서입니다."}
    ]


# 3. 화면에 이전 대화 내용 출력 (시스템 메시지 제외)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. 채팅 입력창 및 로직
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 입력 화면 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # 스트리밍 효과를 위한 공간
        
        try:
            # API 호출
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                stream=True # 스트리밍 활성화
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌") # 타이핑 효과
            
            message_placeholder.markdown(full_response)
            
            # 기록에 답변 추가
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # 메모리 관리 (최신 10개 유지)
            if len(st.session_state.messages) > 11:
                st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-10:]

        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")