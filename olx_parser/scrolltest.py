from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--enable-chrome-browser-cloud-management")


driver = webdriver.Chrome(options=chrome_options)


url = "https://www.olx.uz/nedvizhimost/kvartiry/prodazha/tashkent/"

driver.get(url)

time.sleep(10)

for page in range(1, 6):

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


        time.sleep(15)

    except Exception as e:
        print(f"An error occurred: {e}")
        break


driver.quit()
