from fastapi import FastAPI
import uvicorn
from trainings_app.routers import users, clients

app = FastAPI()

app.include_router(router=users.router)
app.include_router(router=clients.router)

if __name__ == "__main__":
    uvicorn.run("trainings_app.main:app")
