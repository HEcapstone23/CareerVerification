from selenium import webdriver # 동적페이지(js등)를 처리하기 위한 크롤링 라이브러리
from bs4 import BeautifulSoup
import time
import source.ext_career as ext2

def patent_ver(webdriver_path, keyword, verification_list):

    # Chrome WebDriver 서비스 설정
    service = webdriver.chrome.service.Service(executable_path=webdriver_path)

    # 웹 드라이버 초기화
    driver = webdriver.Chrome(service=service)

    # 가져올 웹 페이지의 URL
    url = 'http://kportal.kipris.or.kr/kportal/search/total_search.do' # 키프리스 특허정보검색서비스

    # 웹 페이지 열기
    driver.get(url)
    # time.sleep(2) #결과값확인 -> 창이 뜨는지 확인하기 위함
    input_xpath = '//*[@id="searchKeyword"]'

    #검색창에 텍스트 입력
    input_element = driver.find_element("xpath", input_xpath) # 셀레니움 함수변경으로 인해 find_element 사용 -> 이전 버전 find_element_by_xpath
    input_element.send_keys(keyword)
    time.sleep(5) #결과값 확인 -> 텍스트가 입력되는지 확인

    #버튼 클릭
    button_xpath = '//*[@id="initSearchResultPageFrmNewBookMark"]/img'
    button_element = driver.find_element("xpath", button_xpath)
    button_element.click()
    time.sleep(5) #결과값 확인 -> 텍스트가 입력되는지 확인

    # 웹 페이지의 HTML 내용 가져오기
    html_content = driver.page_source

    # 웹 드라이버 종료
    driver.quit()

    # print(html_content) #웹페이지 html출력확인
    print(type(html_content))

    #html처리를 위해 beautifulsoup 사용
    soup = BeautifulSoup(html_content, 'html.parser')
    found = False
    for verification in verification_list:
        if verification in soup.text:
            found = True
            break

    if found:
        ext2.vres['patent'].append("특허 정보가 있습니다.")
        #print("해당 지원자의 정보가 있습니다.")
    else:
        ext2.vres['patent'].append("특허 정보가 없습니다.")
        #print("해당 지원자의 정보가 없습니다.")
    
    print(ext2.vres) # 검증 결과 딕셔너리 확인용