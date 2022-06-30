
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, validator
from enum import Enum
from .models import shopunit


class DateType(BaseModel):
    date: datetime

class StatisticRequest(BaseModel):
    dateStart: datetime
    dateEnd: datetime

class ShopUnitType(str, Enum):
    offer = 'OFFER'
    category = 'CATEGORY'

class ShopUnit(BaseModel):
    id: UUID
    name: str
    date: datetime
    parentId: UUID
    type: ShopUnitType
    price: int
    children: List

class ShopUnitImport(BaseModel):

    id: UUID
    name: str
    parentid: UUID = None
    type: ShopUnitType
    price: int = None

    @validator('price')
    def null_price_if_category(cls, field_value, values, field, config):
        if values['type'] == ShopUnitType.category and field_value is not None :
            raise ValueError('Price for category must be Null')
        
        if values['type'] == ShopUnitType.offer and (field_value is None or field_value < 0) :
            raise ValueError('Price for offer must > 0')
        return field_value
            
    class Meta:
        orm_model = shopunit.ShopUnitModel


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: UUID
    type: ShopUnitType
    price: int
    date: datetime
    children: List

class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]


class Error(BaseModel):
    code: int
    message: str