import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def crawl_real_estate(url):
    print(f"Fetching URL: {url}")
    # Chrome options 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # ChromeDriver 설치 및 실행
    chrome_version = "125.0.6422.113"  # 최신 크롬 버전을 수동으로 지정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=chrome_version).install()), options=chrome_options)
    driver.get(url)
    
    # 페이지가 로드될 때까지 잠시 대기
    time.sleep(5)
    
    # 매물 정보를 저장할 리스트
    property_list = []

    # 매물 리스트를 찾습니다.
    items = driver.find_elements(By.CSS_SELECTOR, '.item_inner')
    print(f"Found {len(items)} items")

    for idx, item in enumerate(items):
        try:
            print(f"Processing item {idx + 1}")
            title = item.find_element(By.CSS_SELECTOR, '.item_title .text').text.strip()
            price = item.find_element(By.CSS_SELECTOR, '.price_line .price').text.strip()
            info_areas = item.find_elements(By.CSS_SELECTOR, '.info_area .line .spec')

            info_area_1 = info_areas[0].text.strip() if len(info_areas) > 0 else ''
            info_area_2 = info_areas[1].text.strip() if len(info_areas) > 1 else ''

            agent_info_1 = item.find_elements(By.CSS_SELECTOR, '.cp_area .agent_name')[0].text.strip() if len(item.find_elements(By.CSS_SELECTOR, '.cp_area .agent_name')) > 0 else ''
            agent_info_2 = item.find_elements(By.CSS_SELECTOR, '.cp_area .agent_name')[1].text.strip() if len(item.find_elements(By.CSS_SELECTOR, '.cp_area .agent_name')) > 1 else ''

            tag = item.find_element(By.CSS_SELECTOR, '.tag_area .tag').text.strip() if item.find_elements(By.CSS_SELECTOR, '.tag_area .tag') else ''

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

    driver.quit()
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
