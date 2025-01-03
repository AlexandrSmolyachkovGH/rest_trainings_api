from fastapi import FastAPI
import uvicorn
from trainings_app.routers import users, сlients

app = FastAPI()

app.include_router(router=users.router)

if __name__ == "__main__":
    uvicorn.run("trainings_app.main:app")
