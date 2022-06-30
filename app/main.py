from typing import Any
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ValidationError
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from .schemas import *
from .models.shopunit import Base
from .db import SessionLocal, engine
from . import actions
from .query_validators import BaseValidator


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    return JSONResponse({"code":400, 'message':'Невалидная схема документа или входные данные не верны.','exception':str(exc)}, status_code=400)



@app.post(
    "/imports", response_model=Error, status_code=HTTP_201_CREATED, tags=["imports"]
)
async def import_units(*, db: Session = Depends(get_db), units: ShopUnitImportRequest) -> Any:
    
    await BaseValidator.check_parent(db=db, records=units.items)
    await BaseValidator.type_change(db=db, records=units.items)
    await BaseValidator.unique_id_in_request(db=db, records=units.items)
    
    actions.unit.create(db=db, obj_in=units.items, update_time=units.updateDate)
    return {"code":200, 'message':'Вставка или обновление прошли успешно'}


@app.delete(
    "/delete/{id}",
    response_model=Error,
    responses={HTTP_404_NOT_FOUND: {"model": Error}},
    tags=["delete"],
)

async def delete_post(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    unit = actions.unit.get(db=db, id=id)
    if not unit:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")
    actions.unit.remove(db=db, id=id)
    return {"code":200, 'message':'Удаление прошло успешно'}


@app.get(
    "/nodes/{id}",
    responses={HTTP_404_NOT_FOUND: {"model": Error}},
    tags=["nodes"],
)
async def nodes(*, db: Session = Depends(get_db), id: UUID4) -> Any:

    parent = actions.unit.get(db=db, id=id)
    
    if not parent:
        return JSONResponse({"code":404, "message":"Item not found"}, status_code=404)

    post = actions.unit.nodes(db=db, parent=parent)    
    return post


@app.get(
    "/sales/"
    )
async def sales(*, db: Session = Depends(get_db), date: datetime) -> Any:
    
    return actions.unit.sales(db=db, date=date)

@app.get(
    "/node/{id}/statistic"
    )
async def node_stat(*, db: Session = Depends(get_db), id: UUID4, dateStart: datetime, dateEnd: datetime) -> Any:
    unit = actions.unit.get(db=db, id=id)
    if not unit:
        return JSONResponse({"code":404, "message":"Item not found"}, status_code=404)

    history = actions.unit.get_stat(db=db, id=id, dateStart=dateStart, dateEnd=dateEnd)
    return history
    