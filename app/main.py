import uvicorn
from fastapi import FastAPI
from api.routes import project
from api.routes import resources
from api.routes import images

app = FastAPI()

app.include_router(project.router)
app.include_router(resources.router)
app.include_router(images.router)
