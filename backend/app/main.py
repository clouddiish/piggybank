from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.session import get_session_context
from app.core.seeder import seed_initial_data
from app.routes import role


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_session_context() as session:
        await seed_initial_data(session=session)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(role.router)


@app.get("/")
async def root():
    return {"message": "hello world!"}
