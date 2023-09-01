"""
Main of application
"""

import uvicorn
from fastapi import FastAPI
from app.api.routes import project, resources, images, train_history, test

app = FastAPI()

# Include routers
app.include_router(project.router)
app.include_router(resources.router)
app.include_router(images.router)
app.include_router(train_history.router)
app.include_router(test.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
