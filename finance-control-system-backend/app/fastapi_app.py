from fastapi import FastAPI

from app.db.database import init_db
from app.routers.auth import auth_router
from app.routers.operations import operations_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(operations_router, prefix="/operations", tags=["operations"])



@app.on_event("startup")
async def startup_event():
    await init_db()
