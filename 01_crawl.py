import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_real_estate(url):
    print(f"Fetching URL: {url}")
    # 요청을 보내고 HTML 내용을 가져옵니다.
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {response.status_code}")
        return []

    print("Parsing HTML content")
    soup = BeautifulSoup(response.content, 'html.parser')

    # 매물 정보를 저장할 리스트
    property_list = []

    # 매물 리스트를 찾습니다.
    items = soup.select('.item_inner')
    print(f"Found {len(items)} items")

    for idx, item in enumerate(items):
        try:
            print(f"Processing item {idx + 1}")
            title = item.select_one('.item_title .text').get_text(strip=True)
            price = item.select_one('.price_line .price').get_text(strip=True)
            info_areas = item.select('.info_area .line .spec')

            info_area_1 = info_areas[0].get_text(strip=True) if len(info_areas) > 0 else ''
            info_area_2 = info_areas[1].get_text(strip=True) if len(info_areas) > 1 else ''

            agent_info_1 = item.select('.cp_area .agent_name')[0].get_text(strip=True) if len(item.select('.cp_area .agent_name')) > 0 else ''
            agent_info_2 = item.select('.cp_area .agent_name')[1].get_text(strip=True) if len(item.select('.cp_area .agent_name')) > 1 else ''

            tag = item.select_one('.tag_area .tag').get_text(strip=True) if item.select_one('.tag_area .tag') else ''

            property_list.append({
                'Title': title,
                'Price': price,
                'Info_Area_1': info_area_1,
                'Info_Area_2': info_area_2,
                'Agent_Info_1': agent_info_1,
                'Agent_Info_2': agent_info_2,
                'Tag': tag
            })
            print(f"Processed item {idx + 1}: {title}, {price}")
        except Exception as e:
            print(f"Error processing item {idx + 1}: {e}")

    return property_list

def save_to_excel(data, filename):
    if not data:
        print("No data to save")
        return

    print(f"Saving data to {filename}")
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
