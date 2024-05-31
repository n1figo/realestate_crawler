import requests
import pandas as pd
import os
import time

# 기본 URL (페이지 숫자 부분은 {}로 표시)

base_url = "https://m.land.naver.com/cluster/ajax/articleList?itemId=&mapKey=&lgeo=&showR0=&rletTpCd=APT&tradTpCd=A1&z=14&lat=37.6669&lon=127.0724&btm=37.6358442&lft=127.0190991&top=37.6979428&rgt=127.1257009&totCnt=2176&cortarNo=1135010500&sort=rank&page={}"

# "output" 폴더 생성 (이미 존재한다면 생성하지 않음)
if not os.path.exists('output'):
    os.makedirs('output')

# 데이터프레임 초기화
all_data = pd.DataFrame()

page = 1
while True:
    print(f"페이지 {page} 크롤링 시작...")

    url = base_url.format(page)
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    data = response.json()
    
    # 결과가 없으면 크롤링 중단
    if not data['body']:
        print(f"페이지 {page}에 결과가 없습니다. 크롤링을 중단합니다.")
        break
        
    df = pd.DataFrame(data['body'])
    all_data = pd.concat([all_data, df], ignore_index=True)
    
    # 2초간 대기
    time.sleep(1)
    print(f"페이지 {page} 크롤링 완료!")
    page += 1

    if page == 5:
        break

# "output" 폴더 안에 CSV 파일로 저장
all_data.to_csv('output/naver_land_combined_data.csv', index=False, encoding='cp949')
print("CSV 파일 저장 완료!")
