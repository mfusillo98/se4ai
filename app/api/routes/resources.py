from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# Add resource

class ResourceAdd(BaseModel):
    api_key: str
    name: str
    external: str
    image_urls: list[int] = []


@router.post("/api/projects/{project_id}/resources/add")
def add_resource(project_id, resources: ResourceAdd):
    return project_id


# Delete resource

class ResourceDelete(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/resources/{external_id}/delete")
def delete_resource(project_id, external_id, project: ResourceDelete):
    return {"status": "OK"}