from fastapi import Query
from app.models.shopunit import ShopUnitModel
from .schemas import ShopUnitImport, ShopUnitType
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError, ValidationError


class BaseValidator:

    @staticmethod
    async def check_parent(db: Session, records: ShopUnitImport):
        for record in records:

            if record.id == record.parentid:
                raise ValueError('Item cant have same id and parentId')

            if db.query(ShopUnitModel).filter_by(id=record.parentid).first() is None:

                for idx, parent in enumerate(records):

                    if parent.id == record.parentid and parent.type != ShopUnitType.category:
                        raise ValueError('Parent type in query is not a category')

            elif db.query(ShopUnitModel).filter_by(id=record.parentid).first().type != ShopUnitType.category:
                raise ValueError('Parent type in database is not a category')
        return True

    @staticmethod
    async def type_change(db: Session, records: ShopUnitImport):

        for record in records:
            if db.query(ShopUnitModel).filter_by(id=record.id).first() is None:
                pass
            elif db.query(ShopUnitModel).filter_by(id=record.id).first().type != record.type:
                raise ValueError('Record type cant be changed')

        return True

    @staticmethod
    async def unique_id_in_request(db: Session, records: ShopUnitImport):
        ids = [record.id for record in records]
        if len(set(ids)) != len(ids):
            raise ValueError('Two or more same uuid in request')
        return True