from fastapi import APIRouter
from pydantic import BaseModel
from app.database.database import get_db
import app.api.repository.images as images_repository

router = APIRouter()


# Add resource

class ResourceAdd(BaseModel):
    api_key: str
    name: str
    external_resource_id: str
    images_url: list[str] = []


@router.post("/api/projects/{project_id}/resources/add")
def add_resource(project_id, resource: ResourceAdd):
    db = get_db()
    db.autocommit = False

    query = "SELECT * FROM projects WHERE api_key = '" + resource.api_key + "' AND project_id = " + project_id + ""
    projectStored = db.execute_select(query)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    # Store resource
    query = "INSERT INTO project_resources (name, external_resource_id, project_id) VALUES (%s, %s, %s)"
    values = [resource.name, resource.external_resource_id, project_id]

    resource_id = db.execute_insert(query, values)

    if resource_id is None:
        return {"STATUS": "ERROR", "MESSAGE": "Store failed"}

    # store images
    for img_url in resource.images_url:
        image_id = images_repository.add_resource_image(resource_id, img_url, True)
        if image_id is None:
            return {"STATUS": "ERROR", "MESSAGE": "Image Store failed"}

    db.conn.commit()
    db.close()
    return {"STATUS": "OK", "resource_id": resource_id}


# Delete resource

class ResourceDelete(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/resources/{external_id}/delete")
def delete_resource(project_id, external_id, project: ResourceDelete):
    db = Database()
    db.connect()

    query = "SELECT * FROM projects WHERE api_key = '" + project.api_key + "' AND project_id = " + project_id + ""
    projectStored = db.execute_select(query)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    delete_query = "DELETE FROM project_resources WHERE project_id = %s AND external_resource_id = %s"
    delete_values = (project_id, external_id)

    # Execute the delete query
    deleted_rows = db.execute_delete(delete_query, delete_values)
    if deleted_rows is None:
        return {"STATUS": "ERROR", "message": "Delete undone"}

    db.close()
    return {"STATUS": "OK"}