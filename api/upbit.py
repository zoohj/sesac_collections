import requests
import pandas as pd
import plotly.graph_objects as go

# 1. 업비트 API로 데이터 가져오기
url = "https://api.upbit.com/v1/candles/days?market=KRW-BTC&count=60"
data = requests.get(url).json()

# 2. 데이터프레임 정리
df = pd.DataFrame(data)
df = df.sort_values(by='candle_date_time_kst')

# 3. 캔들차트 생성
fig = go.Figure(data=[go.Candlestick(
    x=df['candle_date_time_kst'],
    open=df['opening_price'],
    high=df['high_price'],
    low=df['low_price'],
    close=df['trade_price'],
    increasing_line_color='red', # 상승봉 색상
    decreasing_line_color='blue' # 하락봉 색상
)])

# 4. 디자인 및 레이아웃 설정
fig.update_layout(
    title='비트코인(BTC/KRW) 캔들차트',
    yaxis_title='가격 (KRW)',
    xaxis_title='날짜',
    xaxis_rangeslider_visible=True, # 하단 범위 조절 슬라이더
    template='plotly_white'
)

fig.show()