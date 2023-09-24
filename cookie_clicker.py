from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = Service(executable_path="D:\Python\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# ID명이 cookie 인 것
cookie = driver.find_element(By.ID,"cookie")

# 클릭 가속성 높이는 옵션의 css tag  store 하위의 div 태그
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]
print(item_ids)

timeout = time.time() + 5
five_min = time.time() + 60*5

while True:
    cookie.click()

    # Every 5sec
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR,"#store b")  # 옵션의 옵션명, 가격체크
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",",""))
                item_prices.append(cost)

        # Create dict of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]  # 가격: 아이템 순서로 데이터생성

        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",","")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id
                print(affordable_upgrades)
        # Purchase the most expensive affordable upgrade
        if affordable_upgrades:
            highest_price_affordable_upgrade = max(affordable_upgrades)
        else:
            highest_price_affordable_upgrade = None   # 업그레이드 직후는 affordable 이 없을 수 있음
        # print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID,to_purchase_id).click()   # ID 찾기의 대상을 가변으로 설정

        # Add another t seconds until the next check
        timeout = time.time() + 5

    #After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break