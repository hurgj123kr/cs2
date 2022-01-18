from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)

# 아래 코드는 크롬 드라이버가 잘실행이 되는지 확인하기
# 구글 이미지 얻어오는 경로
#base_url = 'https://www.google.co.kr/imghp'

# 크롬 옵션 설정
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('lang=ko_KR')
#chrome_options.add_argument('window-size=1980x1080')
#
# 크롬드라이버 경로 자동 지정해줍니다
#driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
#driver.get(base_url)
#driver.implicitly_wait(3)# 3초간격으로 받아옵니다.
#driver.get_screenshot_as_file('google_screen.png')
#driver.close() #확인 결과 잘되었습니다.

# 이미지 스크롤옵션을 지정해서 가져오기


def selenium_scroll_option():
    SCROLL_PAUSE_SEC = 3

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height


# 검색어로 크롤링하기
home_alone = './home_alone/'


# 키워드 검색
search = input('검색할 키워드 입력 :')
image_name = input('저장할 이미지 이름 :')
b = int(input("몇 개 이미지 저장할껀지? : "))
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('http://www.google.co.kr/imghp?hl=ko')
browser = driver.find_element_by_name('q')
browser.send_keys(search)
browser.send_keys(Keys.RETURN)

# 클래스를 찾아서 해당 클래스의 src 리스트 제작
selenium_scroll_option()  # 스크롤하여 이미지를 많이 확보
driver.find_elements_by_xpath(
    '//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input')[0].click()  # 이미지 더보기 클릭
selenium_scroll_option()

# 이미지 src요소를 리스트업해가지고 이미지 url에저장합니다.
# 클래스 이름에서 공백은 .으로 대체해준다.
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
images_url = []
for i in images:
    # src속성에 해당하는 값을 가져옵니다.
    if i.get_attribute('src') != None:
        images_url.append(i.get_attribute('src'))
    else:
        images_url.append(i.get_attribute('data-src'))

driver.close()

# 겹치는 이미지 url을 제거해줍니다.

print('전체 다운로드한 이미지 갯수: {}\n동일한 이미지를 제거한 이미지 갯수:{}'.format(
    len(images_url), len(pd.DataFrame(images_url)[0].unique())))
images_url = pd.DataFrame(images_url)[0].unique()


# 해당하는 파일에 이미지를 다운합니다.
if image_name == 'home_alone':
    for d, url in enumerate(images_url, 0):
        urlretrieve(url, home_alone + image_name + '_' + str(d) + '.jpg')

    driver.close()

