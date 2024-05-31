import requests
from bs4 import BeautifulSoup
import pandas as pd

# pip install requests beautifulsoup4 pandas openpyxl


def crawl_real_estate(url):
    # 요청을 보내고 HTML 내용을 가져옵니다.
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 매물 정보를 저장할 리스트
    property_list = []

    # 매물 리스트를 찾습니다.
    items = soup.select('.item_inner')

    for item in items:
        title = item.select_one('.item_title .text').get_text(strip=True)
        price = item.select_one('.price_line .price').get_text(strip=True)
        info_areas = item.select('.info_area .line .spec')
        
        info_area_1 = info_areas[0].get_text(strip=True) if len(info_areas) > 0 else ''
        info_area_2 = info_areas[1].get_text(strip=True) if len(info_areas) > 1 else ''
        
        agent_info = item.select_one('.cp_area .agent_name').get_text(strip=True)
        
        property_list.append({
            'Title': title,
            'Price': price,
            'Info_Area_1': info_area_1,
            'Info_Area_2': info_area_2,
            'Agent_Info': agent_info
        })

    return property_list

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"크롤링 및 엑셀 파일 저장이 완료되었습니다: {filename}")

if __name__ == "__main__":
    # 노량진동 URL
    url = "https://new.land.naver.com/complexes?ms=37.51245,126.9395,15&a=JGB&e=RETAIL"
    
    # 매물 정보를 크롤링합니다.
    property_data = crawl_real_estate(url)
    
    # 엑셀 파일로 저장합니다.
    output_file = 'NaverRealEstate_Noryangjin.xlsx'
    save_to_excel(property_data, output_file)
