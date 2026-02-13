import asyncio
import time
# 비동기 방식 함수 정의
async def fetch_data_async(name):
    print(f"데이터 조회 시작: {name}")
    await asyncio.sleep(2)  # 2초 동안 제어권을 이벤트 루프에 반환
    print(f"데이터 조회 완료: {name}")

    
# 비동기 실행 메커니즘 확인
async def run_async_example():
    start_time = time.time()
    # 두 개의 비동기 작업을 동시에 예약
    await asyncio.gather(
        fetch_data_async("작업1"),
        fetch_data_async("작업2"),
        fetch_data_async("작업3"),
        fetch_data_async("작업4"),
    )
    end_time = time.time()
    print(f"비동기 총 소요 시간: {end_time - start_time}초")

# 실행 코드
# 비동기 함수의 실행의 asyncio.run()으로 해야하지만, ipynb 또는 colab 환경에서는 이미 이벤트 루프가 돌아가고 있어 대신 await를 활용한다.
# asyncio.run(run_async_example())

asyncio.run(run_async_example())