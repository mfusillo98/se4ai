import json
from fastapi import APIRouter
from pydantic import BaseModel
from app.database.database import get_db
import random
import string
import app.api.repository.projects as projects_repository

router = APIRouter()


# Create project

class ProjectCreateRequest(BaseModel):
    name: str
    selected_features_indexes: list[int] = []


@router.post("/api/projects/create")
def create_project(project: ProjectCreateRequest):
    # Genera api_key
    characters = string.ascii_letters + string.digits
    api_key = ''.join(random.choice(characters) for _ in range(32))

    query = "INSERT INTO projects (name, api_key, selected_features_indexes) VALUES (%s, %s, %s)"
    values = [project.name, api_key, ','.join([str(index) for index in project.selected_features_indexes])]

    db = get_db()
    project_id = db.execute_insert(query, values)
    return {"STATUS": "OK", "project_id": project_id, "api_key": api_key}


# Update project

class ProjectUpdateRequest(BaseModel):
    api_key: str
    name: str
    selected_features_indexes: list[int] = []


@router.post("/api/projects/{project_id}/update")
def update_project(project_id, project: ProjectUpdateRequest):
    db = get_db()

    projectStored = projects_repository.get_project(project_id, project.api_key)
    if projectStored is None:
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

    return {"status": "OK"}


# Features selection

class TrainProjectRequest(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/train")
def train(project_id, request: TrainProjectRequest):
    projectStored = projects_repository.get_project(project_id, request.api_key)
    if projectStored is None:
        return {"STATUS": "ERROR", "message": "Project not found"}
    return projects_repository.train_project(project_id)


class FeatureSelectionRequest(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/apply-training")
def apply_training(project_id, request: FeatureSelectionRequest):
    project = projects_repository.get_project(project_id, request.api_key)
    if project is None:
        return {"STATUS": "ERROR", "message": "Project not found"}
    return projects_repository.apply_training(project)


# Search project

class Search(BaseModel):
    api_key: str
    image: str
    limit: int


@router.post("/api/projects/{project_id}/search")
def search_project(project_id, searchInfo: Search):
    return {"message": "Elenco utenti"}
