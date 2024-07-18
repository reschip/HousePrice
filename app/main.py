from typing import Union

import pickle
import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, logger
from fastapi.middleware.cors import CORSMiddleware


class HouseData(BaseModel):
    MSSubClass: int
    MSZoning: object
    LotFrontage: float
    LotArea: int
    Street: object
    Alley: object
    LotShape:object
    LandContour: object
    Utilities: object
    LotConfig: object
    LandSlope: object
    Neighborhood: object
    Condition1: object
    Condition2: object
    BldgType: object
    HouseStyle: object
    OverallQual: int
    OverallCond:int
    YearBuilt: int
    YearRemodAdd: int
    RoofStyle: object
    RoofMatl: object
    Exterior1st: object
    Exterior2nd: object
    MasVnrType: object
    MasVnrArea: float
    ExterQual: object
    ExterCond: object
    Foundation: object
    BsmtQual: object
    BsmtCond: object
    BsmtExposure: object
    BsmtFinType1: object
    BsmtFinSF1: int
    BsmtFinType2: object
    BsmtFinSF2: int
    BsmtUnfSF: int
    TotalBsmtSF: int
    Heating: object
    HeatingQC: object
    CentralAir: object
    Electrical: object
    stFlrSF: int
    ndFlrSF: int
    LowQualFinSF: int
    GrLivArea: int
    BsmtFullBath:int
    BsmtHalfBath: int
    FullBath: int
    HalfBath: int
    BedroomAbvGr: int
    KitchenAbvGr: int
    KitchenQual: object
    TotRmsAbvGrd: int
    Functional: object
    Fireplaces:int
    FireplaceQu: object
    GarageType: object
    GarageYrBlt: float
    GarageFinish: object
    GarageCars: int
    GarageArea: int
    GarageQual: object
    GarageCond: object
    PavedDrive: object
    WoodDeckSF: int
    OpenPorchSF: int
    EnclosedPorch: int
    SsnPorch: int
    ScreenPorch: int
    PoolArea: int
    PoolQC: object
    Fence: object
    MiscFeature: object
    MiscVal: int
    MoSold: int
    YrSold: int
    SaleType: object
    SaleCondition: object

loaded_model = XGBRegressor()
loaded_model.load_model("model-sklearn.json")


with open('preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello: World"}

@app.get("/predict")
def predict(data: HouseData):
    try:
      
        df = pd.DataFrame([data.model_dump()])


        df.rename(columns={"stFlrSF": "1stFlrSF"}, inplace=True)
        df.rename(columns={"ndFlrSF": "2ndFlrSF"}, inplace=True)
        df.rename(columns={"SsnPorch": "3SsnPorch"}, inplace=True)


        df['totalFSF'] = df['1stFlrSF'] + df['2ndFlrSF'] + df['BsmtFinSF1'] + df['BsmtFinSF2']
        df['ageHouse'] = df['YrSold'] - df['YearBuilt']
        df['overalMult'] = df['OverallQual'] * df['OverallCond']
        df['garageMult'] = df['GarageArea'] * df['GarageCars']
        df['totalPorch'] = df['OpenPorchSF'] + df['WoodDeckSF'] + df['EnclosedPorch'] + df['3SsnPorch'] + df['ScreenPorch']
        df['totalBath'] = df['BsmtFullBath'] + df['BsmtHalfBath']/2 + df['FullBath'] + df['HalfBath']/2
        df['totalAreaSF'] = df['TotalBsmtSF'] + df['GrLivArea']

        df = df.drop(columns=['Alley','PoolQC','Fence','MiscFeature','TotalBsmtSF','GrLivArea','OverallQual','OverallCond','YrSold', 'YearBuilt', 
                              '1stFlrSF', '2ndFlrSF', 'BsmtFinSF1', 'BsmtFinSF2','BsmtFullBath', 'FullBath', 
                              'BsmtHalfBath', 'HalfBath', 'OpenPorchSF', '3SsnPorch', 'EnclosedPorch', 'ScreenPorch',
                              'WoodDeckSF','GarageArea','GarageCars','PoolArea','GarageYrBlt'])

        xprocessed = preprocessor.transform(df)
      
       
        prediction = np.expm1(loaded_model.predict(xprocessed))
        print(prediction)
        return {prediction: prediction}
    except Exception as e:
        print(e)