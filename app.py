import uvicorn
from fastapi import FastAPI
from source.api.auth import router as auth_router
from source.api.user import router as user_router
from source.api.tests import router as tests_router
from source.db import database, engine, metadata
from source.settings import settings

tags_metadata = [
    {
        "name": "Auth",
        "description": "Регистрация, авторизация, профиль"
    },
    {
        "name": "Users",
        "description": "Действия и операции с пользователями"
    },
    {
        "name": "Tests",
        "description": "Действия и операции с тестами"
    }
]

app = FastAPI(
    title="HealthMonitor Test Project",
    description="Test CRUD service for HealthMonitor",
    version="1.0.0b",
    openapi_tags=tags_metadata
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(tests_router)


@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    # metadata.create_all(engine)
    uvicorn.run(
        "app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )


