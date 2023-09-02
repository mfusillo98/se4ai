"""
Routes for operations about images
"""

from fastapi import APIRouter
from pydantic import BaseModel
from app.database.database import get_db
import app.api.repository.images as images_repository


router = APIRouter()


@router.get("/api/projects/{project_id}/resources/{external_id}/images")
def get_images(project_id, external_id):
    """
    Get images
    :param project_id:
    :param external_id:

    :type project_id: int
    :type external_id: int

    :return:
    """
    db = get_db()

    query = "SELECT * FROM projects WHERE project_id = %s"
    values = [project_id]
    projectStored = db.execute_select(query, values)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_resources WHERE external_resource_id = %s AND project_id = %s"
    values = [external_id, project_id]
    resource = db.execute_select(query, values)

    if len(resource) == 0:
        return {"STATUS": "ERROR", "message": "Resource not found"}

    # Store resource
    query = "SELECT * FROM project_resource_images WHERE resource_id = %s"
    values = [str(resource[0]["resource_id"])]
    images = db.execute_select(query, values)

    return {"STATUS": "OK", "images": images}


class ImagesAdd(BaseModel):
    api_key: str
    images_url: list[str] = []


@router.post("/api/projects/{project_id}/resources/{external_id}/images/add")
def add_images(project_id, external_id, imagesAdd: ImagesAdd):
    """
    Add image
    :param project_id:
    :param external_id:
    :param imagesAdd:

    :type project_id: int
    :type external_id: int
    :type imagesAdd: list

    :return:
    """
    db = get_db()
    db.autocommit = False

    query = "SELECT * FROM projects WHERE api_key = %s AND project_id = %s"
    values = [imagesAdd.api_key, project_id]
    projectStored = db.execute_select(query, values)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_resources WHERE external_resource_id = %s AND project_id = %s"
    values = [external_id, project_id]
    resource = db.execute_select(query, values)

    if len(resource) == 0:
        return {"STATUS": "ERROR", "message": "Resource not found"}

    # store images
    for img_url in imagesAdd.images_url:
        image_id = images_repository.add_resource_image(str(resource[0]["resource_id"]), img_url, True)
        if image_id is None:
            return {"STATUS": "ERROR", "MESSAGE": "Image Store failed"}

    db.conn.commit()
    return {"STATUS": "OK"}


class ImagesDelete(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/resources/{external_id}/images/delete")
def delete_image(project_id, external_id, imagesDelete: ImagesDelete):
    """
    Delete images
    :param project_id:
    :param external_id:
    :param imagesDelete:

    :type project_id:
    :type external_id:
    :type imagesDelete:

    :return:
    """
    db = get_db()

    query = "SELECT * FROM projects WHERE api_key = %s AND project_id = %s"
    values = [imagesDelete.api_key, project_id]
    projectStored = db.execute_select(query, values)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_resources WHERE external_resource_id = %s AND project_id = %s"
    values = [external_id, project_id]
    resource = db.execute_select(query, values)

    if len(resource) == 0:
        return {"STATUS": "ERROR", "message": "Resource not found"}

    delete_query = "DELETE FROM project_resource_images WHERE resource_id = %s"
    delete_values = (str(resource[0]["resource_id"]),)

    # Execute the delete query
    deleted_rows = db.execute_delete(delete_query, delete_values)
    if deleted_rows is None:
        return {"STATUS": "ERROR", "message": "Delete undone"}

    return {"STATUS": "OK"}
