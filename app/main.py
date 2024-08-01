import logging
from contextlib import asynccontextmanager
import dotenv

dotenv.load_dotenv()

from http import HTTPStatus

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import status, users
from app.database.engine import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.warning("On startup")
    create_db_and_tables()
    yield
    logging.warning("On shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(status.router)
app.include_router(users.router)


@app.get("/", status_code=HTTPStatus.OK)
def service_status() -> dict[str, str]:
    return {"message": "Service is running"}


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)
