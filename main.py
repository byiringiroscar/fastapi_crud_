from fastapi import FastAPI, Body, Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session


# if we don't have database it will create new 1 by using engine we created
Base.metadata.create_all(engine)

# function which will help us to access to the database and session

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

# http://127.0.0.1:8000/docs#/ this help you to run the swagger UI as testing

fakeDatabase = {
    1: {'task': "clean code"},
    2: {'task': "Write blog"},
    3: {'task': "keep time"},
    4: {'task': "zarus pip"},
}


@app.get("/item")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


# get one item by using database and tables

@app.get("/{id}")
def getItem(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


# options 1 for post
@app.post("/")
def addItem(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# put request by getting data in table

@app.put("/{id}")
def updateItem(id: int, item: schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

# delete request

@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()

    return "Item was deleted"


# ================== here we were using fakedatabase as our data =============
#
# fakeDatabase = {
#     1: {'task': "clean code"},
#     2: {'task': "Write blog"},
#     3: {'task': "keep time"},
#     4: {'task': "zarus pip"},
# }
#
#
# @app.get("/")
# def getItems():
#     return fakeDatabase
#
#
# # get one item
#
# @app.get("/{id}")
# def getItem(id: int):
#     return fakeDatabase[id]
#
#
# # options 1 for post
# @app.post("/")
# def addItem(task: str):
#     new_id = len(fakeDatabase.keys()) + 1
#     fakeDatabase[new_id] = {"task": task}
#     return fakeDatabase
#
#
# # put request
#
# @app.put("/{id}")
# def updateItem(id: int, item: schemas.Item):
#     fakeDatabase[id]['task'] = item.task
#     return fakeDatabase
#
# # delete request
#
# @app.delete("/{id}")
# def deleteItem(id: int):
#     del fakeDatabase[id]
#     return fakeDatabase

# option 3 for post by using Body method
# @app.post("/")
# def addItem(body = Body()):
#     new_id = len(fakeDatabase.keys()) + 1
#     fakeDatabase[new_id] = {"task": body['task']} # item.task we are moving in class Item
#     return fakeDatabase


# option 2 for post
# here is post method but when we will have many data to post it will be messy to put it on parameters so whe use pydantic
# @app.post("/")
# def addItem(item: schemas.Item):
#     new_id = len(fakeDatabase.keys()) + 1
#     fakeDatabase[new_id] = {"task": item.task} # item.task we are moving in class Item
#     return fakeDatabase


# ===========================  end of using fake database ================================
