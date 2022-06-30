from datetime import timedelta
from typing import Generic, List, Optional, Type, TypeVar
from app.db_scripts.nodes import script
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.shopunit import ShopUnitModel, ChangeHistory
from .schemas import *
from .db import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseActions(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):

        self.model = model

   
    def get(self, db: Session, id: UUID4) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType, update_time: datetime) -> ModelType:
        models_array = []
        for obj in obj_in:
            obj_in_data = jsonable_encoder(obj)
            obj_in_data.update({'date':update_time})

            models_array.append(obj_in_data)

        self.log_old(db=db, models=models_array)
        self.sess_to_db(db=db,array=models_array)

        return 0

    def log_old(self, db: Session, *, models: List):
        out: List = []
        for model in models:
            vars = (jsonable_encoder(self.get(db=db,id=model['id'])))
            if vars:
                out.append(ChangeHistory(**vars))
        self.sess_to_db(db=db,models=out)


    def sess_to_db(self, db: Session, *, array: List = None, models: List[ChangeHistory] = None):
        with db as sess:
            if array:
                for model in array:
                    entity = ShopUnitModel(**model)
                    sess.merge(entity)
            elif models:
                for model in models:
                    sess.merge(model)
            db.commit()

    def get_stat(self, db: Session, *, id: UUID4, dateStart:datetime, dateEnd: datetime):
        print(dateStart, dateEnd)
        history = db.query(ChangeHistory).filter(and_(ChangeHistory.date>=dateStart, ChangeHistory.date<dateEnd, ChangeHistory.id==id)).order_by(ChangeHistory.date).all()
        history = jsonable_encoder(history)
        return {'items':history}


    

    def remove(self, db: Session, *, id: UUID4) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.query(ChangeHistory).filter_by(id=id).delete()
        db.commit()
        return obj



    def nodes(self, db: Session, *, parent: ShopUnitModel) -> ModelType:
        records = db.execute(script % parent.id).first()
        if records:
            records = jsonable_encoder(records)
            items = jsonable_encoder(parent)
            items.update(records)
            recr(items)
        else:
            items = jsonable_encoder(parent)
            items.update({'children':[]})
        return items


    def sales(self, db: Session, *, date: datetime) -> ModelType:
        yesterday = date - timedelta(days = 1)
        Model = self.model
        records = db.query(Model).filter(and_(Model.date<date, Model.date>=yesterday, Model.type=='offer')).all()
        return {'items': jsonable_encoder(records)}
            

def recr(obj):
    if obj['type'] == 'offer':
        del obj['children']
    try:
        if obj['children']:
            for e in obj['children']:
                recr(e)
    except:
        return 0
        
        



class UnitActions(BaseActions[ShopUnitModel,ShopUnitImport,ShopUnitImport]):
    pass


unit = UnitActions(ShopUnitModel)