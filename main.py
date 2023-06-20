from fastapi import FastAPI
from api.routes import project
from api.routes import resources
from api.routes import images
from database.database import Database

app = FastAPI()

app.include_router(project.router)
app.include_router(resources.router)
app.include_router(images.router)