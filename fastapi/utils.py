from catboost import CatBoostRegressor
from sklearn.preprocessing import RobustScaler
import joblib
import numpy as np
from typing import List, Union
import pandas as pd

model = CatBoostRegressor()
model.load_model('model/catboost_model.bin')

scaler = joblib.load('model/robust_scaler.pkl')


def ohe(input_list: list):
    columns = ['rooms', 'allArea', 'floor', 'floorsNumber', 'type_Бизнес',
       'type_Частное_лицо', 'housingType_Вторичный_рынок',
       'housingType_Новостройки', 'buildingType_Блочный',
       'buildingType_Деревянный', 'buildingType_Кирпичный',
       'buildingType_Монолитный', 'buildingType_Панельный',
       'planType_Малосемейка', 'planType_Многоуровневая', 'planType_Пентхаус',
       'planType_Раздельная', 'planType_Смежная', 'planType_Смежно-раздельная',
       'planType_Студия', 'bathroom_2_санузла_и_более', 'bathroom_Раздельный',
       'bathroom_Совмещенный', 'setOfFurniture_Да', 'setOfFurniture_Нет',
       'repairType_Авторский_проект', 'repairType_Евроремонт',
       'repairType_Предчистовая_отделка', 'repairType_Средний',
       'repairType_Требует_ремонта', 'repairType_Черновая_отделка',
       'district_Алмазарский_район', 'district_Бектемирский_район',
       'district_Мирабадский_район', 'district_Мирзо-Улугбекский_район',
       'district_Сергелийский_район', 'district_Учтепинский_район',
       'district_Чиланзарский_район', 'district_Шайхантахурский_район',
       'district_Юнусабадский_район', 'district_Яккасарайский_район',
       'district_Яшнабадский_район', 'comission_Да', 'comission_Нет']

    df = pd.DataFrame(columns=columns)

    new_row = dict.fromkeys(columns, 0)

    for i in range(4):
        new_row[columns[i]] = input_list[i]

    for i, value in enumerate(input_list[4:], start=4):
        if i == 9:
            new_row[f'setOfFurniture_{value}'] = 1
        elif i == 12:
            new_row[f'comission_{value}'] = 1
        else:
            for col in columns:
                if str(value) in col:
                    new_row[col] = 1

    X = pd.DataFrame([new_row], columns=columns)
    return X

def scale_and_predict(X: pd.DataFrame):
    columns_to_scale = X.columns[:4]
    X_to_scale = X[columns_to_scale]
    X_scaled_partial = scaler.transform(X_to_scale)
    X_scaled_partial_df = pd.DataFrame(X_scaled_partial, columns=columns_to_scale)
    X.loc[:, columns_to_scale] = X_scaled_partial_df

    prediction = model.predict(X)

    return np.round(prediction, 2)

#a = [3.0, 25.0, 3.0, 4.0, 'Частное_лицо', 'Вторичный_рынок', 'Кирпичный', 'Малосемейка', 'Совмещенный', 'Да', 'Евроремонт', 'Сергелийский_район', 'Нет']
#print({"result": ohe(a)})
#print(scale_and_predict(ohe(a)))
