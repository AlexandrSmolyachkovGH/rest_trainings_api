from fastapi import FastAPI
import uvicorn
from trainings_app.routers import r_users, r_сlients

app = FastAPI()

app.include_router(router=r_users)

if __name__ == "__main__":
    uvicorn.run("trainings_app.main:app")
