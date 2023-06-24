import json
from fastapi import APIRouter
from pydantic import BaseModel
from app.database.database import get_db
import random
import string

router = APIRouter()


# Create project

class ProjectCreate(BaseModel):
    name: str
    selected_features_indexes: list[int] = []


@router.post("/api/projects/create")
def create_project(project: ProjectCreate):
    # Genera api_key
    characters = string.ascii_letters + string.digits
    api_key = ''.join(random.choice(characters) for _ in range(32))

    query = "INSERT INTO projects (name, api_key, selected_features_indexes) VALUES (%s, %s, %s)"
    values = [project.name, api_key, ','.join([str(index) for index in project.selected_features_indexes])]

    db = get_db()
    project_id = db.execute_insert(query, values)
    db.close()
    return {"STATUS": "OK", "project_id": project_id, "api_key": api_key}


# Update project

class ProjectUpdate(BaseModel):
    api_key: str
    name: str
    selected_features_indexes: list[int] = []


@router.post("/api/projects/{project_id}/update")
def update_project(project_id, project: ProjectUpdate):
    db = get_db()

    query = "SELECT * FROM projects WHERE api_key = '" + project.api_key + "' AND project_id = " + project_id + ""
    projectStored = db.execute_select(query)

    if len(projectStored) == 0:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "UPDATE projects SET name = %s, selected_features_indexes = %s WHERE project_id = %s"
    # If values are new I update them
    values = (

        project.name if project.name is not None else projectStored[0].name,

        ','.join([str(index) for index in project.selected_features_indexes])
        if project.selected_features_indexes is not None
        else ','.join([str(index) for index in project.selected_features_indexes]),

        project_id
    )

    rows_affected = db.execute_update(query, values)
    if rows_affected is None:
        return {"STATUS": "ERROR", "message": "Update failed"}

    db.close()
    return {"status": "OK"}


# Features selection

class FeatureSelection(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/feature-selection")
def feature_selection(project_id, api_key: FeatureSelection):
    return {"message": "Elenco utenti"}


# Search project

class Search(BaseModel):
    api_key: str
    image: str
    limit: int


@router.post("/api/projects/{project_id}/search")
def search_project(project_id, searchInfo: Search):
    return {"message": "Elenco utenti"}
