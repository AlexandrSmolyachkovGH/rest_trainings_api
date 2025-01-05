from fastapi import FastAPI
import uvicorn
from trainings_app.routers import users, сlients
from db.connection import connect_to_db, close_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db()


app.include_router(router=users.router)

if __name__ == "__main__":
    uvicorn.run("trainings_app.main:app")
