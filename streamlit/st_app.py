import streamlit as st
import requests

st.write("""
# Предсказание цены на квартиру в Ташкенте
Введите данные
""")

rooms = st.number_input("Количество комнат", value=None)

area = st.number_input("Общая площадь", value=None)

floor = st.number_input("Этаж", value=None)

floorNumber = st.number_input("Этажность дома", value=None)

seller_type = st.selectbox(
    'Выберите тип продажи',
    ('Частное лицо', 'Бизнес'),
        index=None)

housingType = st.selectbox(
    'Выберите тип жилья',
    ('Вторичный рынок', 'Новостройки'),
        index=None)

buildingType = st.selectbox(
    'Выберите тип строения',
    ('Блочный', 'Деревянный', 'Кирпичный',
      'Монолитный', 'Панельный'),
        index=None)

planType = st.selectbox(
    'Выберите тип планировки',
    ('Малосемейка', 'Многоуровневая', 'Пентхаус',
      'Раздельная', 'Смежная', 'Смежно-раздельная', 'Студия'),
        index=None)

bathroom = st.selectbox(
    'Выберите тип санузла',
    ('Раздельный', 'Совмещенный', '2 санузла и более'),
        index=None)

furniture = st.selectbox(
    'Меблирована?',
    ('Да', 'Нет',),
        index=None)

repairType = st.selectbox(
    'Выберите тип ремонта',
    ('Авторский проект', 'Евроремонт', 'Предчистовая отделка',
      'Средний', 'Требует ремонта', 'Черновая отделка'),
        index=None)

district = st.selectbox(
    'Выберите район',
    ('Алмазарский район', 'Бектемирский район', 'Мирабадский район',
      'Мирзо-Улугбекский район', 'Сергелийский район', 'Учтепинский район',
      'Чиланзарский район', 'Шайхантахурский район', 'Юнусабадский район',
      'Яккасарайский район', 'Яшнабадский район'),
        index=None)

commission = st.selectbox(
    'Есть комиссия?',
    ('Нет', 'Да'),
        index=None)



if st.button('Посчитать'):
    values_list = []
    values_list.append(rooms)
    values_list.append(area)
    values_list.append(floor)
    values_list.append(floorNumber)
    values_list.append(seller_type)
    values_list.append(housingType)
    values_list.append(buildingType)
    values_list.append(planType)
    values_list.append(bathroom)
    values_list.append(furniture)
    values_list.append(repairType)
    values_list.append(district)
    values_list.append(commission)

    response = requests.post("http://fastapi:8001/predict", json=values_list)

    if response.status_code == 200:
        result = response.json()["result"]
        st.write("Цена:", result[0])
    else:
        st.write("Error occurred while processing the request.")