from typing import List, Optional
import datetime
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class ShopUnitType(str,Enum):
    # OFFER, CATEGORY
    offer = 'OFFER'
    category = 'CATEGORY'

    class Config:
        description = 'Тип элемента - категория или товар'
        

# class ShopUnit(BaseModel):
#     id: UUID
#     name: str


# class ShopUnitImport(ShopUnit):
#     items: List[ShopUnit]
#     parentId: Optional[UUID] = None
#     type: ShopUnitType
#     price: Optional[int] = None

#     class Config:  
#         use_enum_values = True