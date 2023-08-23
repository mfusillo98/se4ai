import uvicorn
from fastapi import FastAPI
from app.api.routes import project
from app.api.routes import resources
from app.api.routes import images
from app.api.routes import train_history
from app.api.routes import test

app = FastAPI()

app.include_router(project.router)
app.include_router(resources.router)
app.include_router(images.router)
app.include_router(train_history.router)
app.include_router(test.router)
