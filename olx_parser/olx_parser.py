from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sqlite3 as sq
from utils import data_parse
from utils import data_insert

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--enable-chrome-browser-cloud-management")


driver = webdriver.Chrome(options=chrome_options)


# Ссылка на страницу с объявлениями
url = "https://www.olx.uz/nedvizhimost/kvartiry/prodazha/tashkent/"


driver.get(url)

# Ждем, пока страница полностью загрузится
time.sleep(5)

# Получаем ссылки на объявления
for page in range(1, 25):

    ad_links = driver.find_elements(By.XPATH, "//a[@class='css-rc5s2u']")

    for ad_link in ad_links:
        ad_url = ad_link.get_attribute("href")
        parsed_dict = data_parse(ad_url)
        data_insert(parsed_dict)
        


    try:
        pagination_forward_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-forward']")
        driver.execute_script("arguments[0].scrollIntoView();", pagination_forward_button)

        time.sleep(10)
        driver.execute_script("window.scrollBy(0, -200);")

        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView();", pagination_forward_button)
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, -200);")

        button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-forward']")
        button.click()


        # Дожидаемся загрузки следующей страницы
        time.sleep(15)

    except Exception as e:
        print(f"An error occurred: {e}")
        break


driver.quit()
