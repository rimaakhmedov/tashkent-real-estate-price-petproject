from fastapi import FastAPI, HTTPException
from typing import List, Union
from utils import scale_and_predict, ohe
import pandas as pd
import numpy as np


app = FastAPI()


@app.post("/predict")
async def make_predict(vlist: List[Union[str, float]]):
    try:
        ohe_df = ohe(vlist)
        print(ohe_df.to_dict(orient="records"))
        pred = scale_and_predict(ohe_df)
        print(pred)
        return {"result": pred.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))