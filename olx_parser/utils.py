from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
from bs4 import BeautifulSoup
import sqlite3 as sq
import re


def find_element(soup, label):
    ul_tag = soup.find('ul', class_='css-sfcl1s')
    if ul_tag:
        li_tags = ul_tag.find_all('li', class_='css-1r0si1e')
    
        for li_tag in li_tags:
            p_tag = li_tag.find('p', class_='css-b5m1rv er34gjf0')
            if p_tag and label in p_tag.get_text():
                type = p_tag.get_text(strip=True)
                type = type.split(":")[1].strip()
                return type
    else:
        return None



def data_parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ad_id_span = soup.find('span', class_='css-12hdxwj er34gjf0')
    ad_id = int(re.findall(r'\b\d+\b', ad_id_span.get_text(strip=True))[0]) if ad_id_span else None

    ad_title = soup.find('h4', class_='css-1juynto').text if soup.find('h4', class_='css-1juynto') else None

    description_div = soup.find('div', class_='css-1t507yq er34gjf0')
    description = description_div.get_text(strip=True) if description_div else None

    ul_tag = soup.find('ul', class_='css-sfcl1s')
    if ul_tag:
        li_tags = ul_tag.find_all('li', class_='css-1r0si1e')
    
        for li_tag in li_tags:
            p_tag = li_tag.find('p', class_='css-b5m1rv er34gjf0')
            if p_tag:
                span_tag = p_tag.find('span')
                if span_tag:
                    seller_type = span_tag.get_text(strip=True)
                    break
    else:
        seller_type = None


    housingType = find_element(soup, 'Тип жилья')
    rooms_number = int(find_element(soup, 'Количество комнат')) if find_element(soup, 'Количество комнат') else None
    allArea = find_element(soup, 'Общая площадь')
    livingArea = find_element(soup, 'Жилая площадь')
    kitchenArea = find_element(soup, 'Площадь кухни')
    floor = find_element(soup, 'Этаж')
    floorNumber = find_element(soup, 'Этажность дома')
    buildingType = find_element(soup, 'Тип строения')
    planType = find_element(soup, 'Планировка')
    sanUzel = find_element(soup, 'Санузел')
    furn = find_element(soup, 'Меблирована')
    inQuart = find_element(soup, 'В квартире есть')
    nearestStruct = find_element(soup, 'Рядом есть')
    repairType = find_element(soup, 'Ремонт')

    #Получаем район
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    html_code = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html_code, 'html.parser')
    location_span = soup.find('span', class_='css-1c0ed4l')
    location_text = location_span.get_text(strip=True) if location_span else None

    comis = find_element(soup, 'Комиссионные')

    #Получаем цену
    price_h3 = soup.find('h3', class_='css-12vqlj3')
    price = price_h3.get_text(strip=True) if price_h3 else None

    data_dict = {
        "id": ad_id, "title": ad_title, "description": description, "type": seller_type, 
        "housingType": housingType, "rooms": rooms_number, "allArea": allArea, "privateArea": livingArea,
        "kitchenArea": kitchenArea, "floor": floor, "floorsNumber": floorNumber,
        "buildingType": buildingType, "planType": planType, "bathroom": sanUzel,
        "setOfFurniture": furn, "inQuart": inQuart, "nearestStructures": nearestStruct,
        "repairType": repairType, "district": location_text, "comission": comis, "price": price
    }

    return data_dict


def data_insert(data_dict: dict):

    sqlite_connection = sq.connect("tash_prices.db")
    cursor = sqlite_connection.cursor()

    cursor.execute("SELECT id FROM olx WHERE id = :id", {"id": data_dict["id"]})
    existing_id = cursor.fetchone()

    if existing_id is None:
        # Если объявление с таким id не существует, выполняем вставку
        cursor.execute("""INSERT INTO olx
                       (id, title, description, type, housingType, rooms, 
                       allArea, privateArea, kitchenArea, floor, floorsNumber,
                       buildingType, planType, bathroom, setOfFurniture, inQuart, nearestStructures,
                       repairType, district, comission, price)
                        VALUES (:id, :title, :description,
                       :type, :housingType, :rooms, :allArea, :privateArea, :kitchenArea, :floor, 
                       :floorsNumber, :buildingType, :planType, :bathroom, :setOfFurniture, :inQuart, 
                       :nearestStructures, :repairType, :district, :comission, :price)""", data_dict)

        sqlite_connection.commit()
        print(f'Квартира {data_dict["id"]} добавлена в БД')
    else:
        # Если объявление с таким id уже существует, вы можете выполнить нужные действия
        print(f'Объявление с id {data_dict["id"]} уже существует в БД')

    cursor.close()

    

     


    





