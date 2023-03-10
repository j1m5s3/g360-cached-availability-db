from fastapi import APIRouter, Body, Request, Response, HTTPException, status, FastAPI
from fastapi.encoders import jsonable_encoder
from typing import List

from dotenv import dotenv_values
from pymongo import MongoClient

from api.getters import router as getters_router

config = dotenv_values(".env")
app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config['DB_CONNECTION_URL'])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(getters_router)
