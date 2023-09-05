"""
Routes for operations about resources
"""

from fastapi import APIRouter
from pydantic import BaseModel
from app.database.database import get_db
import app.api.repository.images as images_repository
from utils import metrics

router = APIRouter()


# Add resource

class ResourceAdd(BaseModel):
    api_key: str
    name: str
    external_resource_id: str
    images_url: list[str] = []


@router.post("/api/projects/{project_id}/resources/add")
def add_resource(project_id, resource: ResourceAdd):
    """
    Add a new resource
    :param project_id:
    :param resource:

    :type project_id:
    :type resource:

    :return:
    """
    try:
        db = get_db()
        db.autocommit = False

        query = "SELECT * FROM projects WHERE api_key = %s AND project_id = %s"
        values = [resource.api_key, project_id]
        projectStored = db.execute_select(query, values)

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
    except Exception as e:
        return {"STATUS": "ERROR", "message": "Error: "+str(e)}

    metrics.metrics['resources_created_total'].inc()
    return {"STATUS": "OK", "resource_id": resource_id}


# Delete resource

class ResourceDelete(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/resources/{external_id}/delete")
def delete_resource(project_id, external_id, project: ResourceDelete):
    """
    Delete a resource
    :param project_id:
    :param external_id:
    :param project:

    :type project_id:
    :type external_id:
    :type project:

    :return:
    """
    db = get_db()
    db.connect()

    query = "SELECT * FROM projects WHERE api_key = %s AND project_id = %s"
    values = [project.api_key, project_id]
    projectStored = db.execute_select(query, values)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    delete_query = "DELETE FROM project_resources WHERE project_id = %s AND external_resource_id = %s"
    delete_values = (project_id, external_id)

    # Execute the delete query
    deleted_rows = db.execute_delete(delete_query, delete_values)
    if deleted_rows is None:
        return {"STATUS": "ERROR", "message": "Delete undone"}

    return {"STATUS": "OK"}