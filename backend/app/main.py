from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.session import get_session_context
from app.core.seeder import seed_initial_data
from app.routes import role, security, type, user, category, transaction, goal


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
app.include_router(security.router)
app.include_router(user.router)
app.include_router(type.router)
app.include_router(category.router)
app.include_router(transaction.router)
app.include_router(goal.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "hello world!"}
