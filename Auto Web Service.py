from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from time import sleep



# 웹 페이지의 소스코드를 파싱하기 위해 Beatiful Soup 라이브러리
from bs4 import BeautifulSoup
'''
웹페이즈를 크롤링해서 상품을 주문하는 py파일
주의사항.
# 크롤링이 누적될 시 임시파일들을 삭제해서 최적화를 해야한다.
# 접속폭주로인한 exception 처리를 해줘야한다. 예시)재검색, query response가 올 때까지 대기 등
'''
'''
=목적=
위메프용
직접 해당 페이지 주소 입력으로 빠르게 1번 옵션만을 선택하여 구매하는 함수. 
최대한 빠르게 옵션을 모를때 구매하는 함수.(일단사자용)

=작성자=
extremecode

=수정일=
2019-04-18
'''

# 크롬 웹 드라이버 실행
driver = webdriver.Chrome('C:\ChromeDriver\chromedriver.exe')

def auto_purchase_wemake(p_url):
    url = p_url
    driver.get(url)
    driver_implicitly_wait(60)

    for num1 in range(1, 5):
        try:
            Option1 = driver.find_element_by_xpath(
                '//*[@id="dealOnecutOption"]/div/div[' + str(num1) + ']/a')
            driver_implicitly_wait(10)
        except NoSuchElementException:
            break

        if not Option1.text:
            break
        else:
            if num1 == 1:
                Option1.click()
                driver_implicitly_wait(10)
            for num2 in range(1, 5):
                try:
                    Option2 = driver.find_element_by_xpath(
                        '//*[@id="dealOnecutOption"]/div/div[' + str(num1) + ']/ul/li[' + str(num2) + ']/a')
                    sleep(0.5)
                except NoSuchElementException:
                    break
                if Option2.text == '':
                    break
                else:
                    Option2.click()
                    driver_implicitly_wait(10)
                    break

    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div/div[2]/div[1]/div[6]/a[2]').click()
    return 0

def driver_implicitly_wait(p_time):
    try:
        driver.implicitly_wait(p_time)
    except Exception as e:
        print('대기 오류', e)
    return 0

#접속 사이트
main_url = 'http://www.wemakeprice.com/'
# 검색키워드
search_keyword = '헤드셋'
# 정확한 포함 키워드 및 가격영역
search_acc_keyword = ''
search_acc_price = 0

# 상품 정보를 담는 리스트 (ItemInfo 리스트)
from Items import ItemInfo
item_list = []

# 사이트 접속
driver.get(main_url)

driver_implicitly_wait(10)

# 검색창을 찾아서 키워드 입력.
driver.find_element_by_id('searchKeyword').send_keys(search_keyword)

# 검색 버튼 클릭
driver.find_element_by_xpath('//*[@id="search_keyword_btn"]/button').click()


try:
    driver_implicitly_wait(60)

    ## 명시적 대기 . 특정 요소가 로케이트 (발견될때까지) 대기
    # element = WebDriverWait(driver, 10).until(
    #     # 지정한 한개 요소가 올라오면 웨이트 종료. (물품 영역이 로딩될때까지 대기)
    #     Ec.presence_of_element_located( By.ID, 'search_ad_area')
    # )
    # element = WebDriverWait(driver, 10).until(
    #     # 지정한 한개 요소가 올라오면 웨이트 종료. (물품 영역이 로딩될때까지 대기)
    #     Ec.presence_of_element_located(By.ID, 'search_deal_area')
    # )
except Exception as e:
    print('대기 오류', e)
# 암묵적 대기 . DOM이 다 로드 될때까지 대기 하고 로드되면 바로 진행.
# try:
#     driver.implicitly_wait(10)
# except Exception as e:
#     print('대기 오류', e)
# 절대적 대기 . time.sleep() : 디도스 방어 솔류션[클라우드 페어]

# 해당 class찾아 타고 타고 내려가서 click함.
#driver.find_element_by_css_selector('.****>.***>***').click()

# 게시판에서 데이터를 가져올때
# 데이터가 많으면 세션(로그인을 해서 접근되는 사이트일 경우) 관리
# 특정 단위별로 로그아웃 로그인 계속 시도
# 특정 게시물이 사라질 경우 => 팝업 발생 -> 팝업 처리 검토.
# 게시판 스캔시 => 임계점을 모름.
# 게시판 스캔 => 메타 정보 획득 => 루프를 돌려서 일괄적으로 방문 접근 처리.

# 자바스크립트 구동하기 테스트
# driver.execute_script('스크립트용코드(%s)'% i)

# 상품명, 기간, 코멘트, 가격, 판매수, 평점, 링크, 썸네일,
try:
    xitems = driver.find_elements_by_css_selector('.section_list>ul>li')

    for li in xitems:
        # print('썸네일 :', li.find_element_by_css_selector('.box_thumb>img').get_attribute('src'))
        # print('상품명 :', li.find_element_by_css_selector('strong.tit_desc').text)
        # print('할인률 :', li.find_element_by_css_selector('span.discount').text)
        # print('가격   :', li.find_element_by_css_selector('span.sale').text)
        # print('판매수 :', li.find_element_by_css_selector('strong.point').text)
        # print('링크   :', li.find_element_by_css_selector('a').get_attribute('href'))
        # print()
        # 데이터 모음
        obj = ItemInfo(li.find_element_by_css_selector('strong.tit_desc').text,
                       li.find_element_by_css_selector('.box_thumb>img').get_attribute('src'),
                       li.find_element_by_css_selector('span.sale').text,
                       li.find_element_by_css_selector('span.discount').text,
                       li.find_element_by_css_selector('strong.point').text,
                       li.find_element_by_css_selector('a').get_attribute('href')
                       )
        item_list.append(obj) # 적제
except Exception as e1:
    print('오류', e1)

    print('상품 총 개수 :', len(item_list))

