from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
from sqlalchemy import Enum
from app.db import Base
from sqlalchemy.orm import mapper


class ShopUnitType(str, enum.Enum):
    offer = 'OFFER'
    category = 'CATEGORY'



class ShopUnitModel(Base):
    __tablename__ = "shopunits"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String)
    date = Column(DateTime)
    parentid = Column('parentid',UUID(as_uuid=True), nullable=True, )
    type = Column(Enum(ShopUnitType))
    price = Column(Integer)

class ChangeHistory(Base):
    __tablename__ = "history"

    pk = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(UUID(as_uuid=True))
    name = Column(String)
    date = Column(DateTime)
    parentid = Column('parentid',UUID(as_uuid=True), nullable=True, )
    type = Column(Enum(ShopUnitType))
    price = Column(Integer)

        