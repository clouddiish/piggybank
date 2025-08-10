from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.session import get_session_context
from app.core.seeder import seed_initial_data
from app.routes import role, security, user


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_session_context() as session:
        await seed_initial_data(session=session)
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.title,
    version=settings.version,
    root_path=settings.api_prefix,
    summary=settings.summary,
    description=settings.description,
)

app.include_router(role.router)
app.include_router(user.router)
app.include_router(security.router)


@app.get("/")
async def root():
    return {"message": "hello world!"}
