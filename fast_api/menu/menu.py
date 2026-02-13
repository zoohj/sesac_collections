import streamlit as st
import base64
import json
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from collections import Counter

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")


# --- UI 설정 ---
st.set_page_config(page_title="커피 주문 집계기", page_icon="☕", layout="wide")
st.title("☕ 단체 주문 데이터 정제 및 집계 시스템")

with st.sidebar:
    st.header("1. 메뉴판 설정")
    uploaded_menu = st.file_uploader(
        "메뉴판 이미지 업로드", type=["jpg", "jpeg", "png"]
    )
    if uploaded_menu:
        st.image(uploaded_menu, caption="참고용 메뉴판", use_container_width=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("2. 댓글 데이터 입력")
    raw_comments = st.text_area("슬랙/카톡 댓글 붙여넣기", height=450)

with col2:
    st.header("3. 분석 및 집계 현황")
    if st.button("🚀 표준화 집계 시작"):
        if not uploaded_menu or not raw_comments:
            st.error("메뉴판 이미지와 댓글 데이터를 모두 입력해주세요.")
        else:
            with st.spinner("AI가 데이터를 정제하고 있습니다..."):
                try:
                    base64_image = encode_image(uploaded_menu)

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": """너는 주문 정제 전문가야. 다음 규칙을 엄격히 지켜:
                                1. 불필요한 정보(이름, 시간 등)는 삭제해.
                                2. 메뉴명은 메뉴판의 정식 명칭을 사용해. (예: 아보카도바나나)
                                3. [사이즈 표준화]: 기본/레귤러는 'R', 플러스/큰거는 'P'로 통일해.
                                4. [온도]: 반드시 'temp' 키를 생성하고 Ice 또는 Hot으로 기록해.
                                5. 중요: 결과는 반드시 'json' 형식으로 {"orders": []} 구조로 반환해.
                                6. 사용자가 별도로 '따뜻하게'라고 말하지 않는 한, 과일 베이스 음료나 에이드, 프레치노는 Ice가 기본이야.
                                7. 온도와 사이즈가 같은 메뉴는 나중에 파이썬이 합칠 수 있게 동일한 텍스트로 생성해.
                                8. **특이사항**: '아보카도바나나'는 메뉴판에 사이즈 구분이 모호하므로 무조건 'R'로 통일해.
                                9. 모든 메뉴명에서 띄어쓰기는 제거해 (예: '아보카도 바나나' -> '아보카도바나나').""",
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"이 데이터를 json으로 정제해줘: {raw_comments}",
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        },
                                    },
                                ],
                            },
                        ],
                        response_format={"type": "json_object"},
                    )

                    raw_json = json.loads(response.choices[0].message.content)
                    refined_list = raw_json.get(
                        "orders",
                        list(raw_json.values())[0]
                        if isinstance(raw_json, dict) and raw_json.values()
                        else [],
                    )

                    if refined_list:
                        # [핵심] 파이썬 집계 로직: 공백 제거 및 대소문자 통일
                        order_keys = []
                        for o in refined_list:
                            menu = str(o.get("menu", "Unknown")).replace(
                                " ", ""
                            )  # 띄어쓰기 제거
                            temp = o.get("temp", "Ice")
                            size = o.get("size", "R")

                            # 아보카도바나나 강제 보정 (AI가 실수할 경우 대비)
                            if "아보카도" in menu:
                                menu = "아보카도바나나"
                                temp = "Ice"
                                size = "R"

                            order_keys.append(f"{menu}|{temp}|{size}")

                        final_counts = Counter(order_keys)

                        # 데이터프레임 구성
                        data_list = []
                        for item, count in final_counts.items():
                            m, t, s = item.split("|")
                            data_list.append(
                                {"메뉴명": m, "온도": t, "사이즈": s, "수량": count}
                            )

                        df = pd.DataFrame(data_list)
                        df = df.sort_values(
                            by="수량", ascending=False
                        )  # 수량 많은 순서로 정렬

                        st.success(f"총 {df['수량'].sum()}개의 주문 분석 완료!")
                        st.table(df)
                        st.bar_chart(df.set_index("메뉴명")["수량"])
                    else:
                        st.warning("분석된 주문 내역이 없습니다.")

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
