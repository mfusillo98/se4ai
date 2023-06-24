from fastapi import APIRouter
from app.database.database import Database
from pydantic import BaseModel
import app.api.repository.images as images_repository


router = APIRouter()


# Get images

@router.get("/api/projects/{project_id}/resources/{external_id}/images")
def get_images(project_id, external_id):
    db = Database()
    db.connect()

    query = "SELECT * FROM projects WHERE project_id = " + project_id + ""
    projectStored = db.execute_select(query)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_resources WHERE external_resource_id = '" + external_id + "' AND project_id = " + project_id + ""
    resource = db.execute_select(query)

    if len(resource) == 0:
        return {"STATUS": "ERROR", "message": "Resource not found"}

    # Store resource
    query = "SELECT * FROM project_resource_images WHERE resource_id = '" + str(resource[0]["resource_id"]) + "'"
    images = db.execute_select(query)

    db.close()
    return {"STATUS": "OK", "images": images}


# Add image

class ImagesAdd(BaseModel):
    api_key: str
    images_url: list[str] = []


@router.post("/api/projects/{project_id}/resources/{external_id}/images/add")
def add_images(project_id, external_id, imagesAdd: ImagesAdd):
    db = Database()
    db.connect()
    db.autocommit = False

    query = "SELECT * FROM projects WHERE api_key = '" + imagesAdd.api_key + "' AND project_id = " + project_id + ""
    projectStored = db.execute_select(query)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_resources WHERE external_resource_id = '" + external_id + "' AND project_id = " + project_id + ""
    resource = db.execute_select(query)

    if len(resource) == 0:
        return {"STATUS": "ERROR", "message": "Resource not found"}

    # store images
    for img_url in imagesAdd.images_url:
        image_id = images_repository.add_resource_image(str(resource[0]["resource_id"]), img_url, True)
        if image_id is None:
            return {"STATUS": "ERROR", "MESSAGE": "Image Store failed"}

    db.conn.commit()
    db.close()
    return {"STATUS": "OK"}


# Delete images

class ImagesDelete(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/resources/{external_id}/images/delete")
def add_images(project_id, external_id, imagesDelete: ImagesDelete):
    db = Database()
    db.connect()

    query = "SELECT * FROM projects WHERE api_key = '" + imagesDelete.api_key + "' AND project_id = " + project_id + ""
    projectStored = db.execute_select(query)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_resources WHERE external_resource_id = '" + external_id + "' AND project_id = " + project_id + ""
    resource = db.execute_select(query)

    if len(resource) == 0:
        return {"STATUS": "ERROR", "message": "Resource not found"}

    delete_query = "DELETE FROM project_resource_images WHERE resource_id = %s"
    delete_values = (str(resource[0]["resource_id"]),)

    # Execute the delete query
    deleted_rows = db.execute_delete(delete_query, delete_values)
    if deleted_rows is None:
        return {"STATUS": "ERROR", "message": "Delete undone"}

    db.close()
    return {"STATUS": "OK"}
