from fastapi import APIRouter
from pydantic import BaseModel
from app.database.database import Database
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

    query = "INSERT INTO projects (name, api_key) VALUES (%s, %s)"
    values = [project.name, api_key]

    db = Database(host='localhost', port='8888', socket='/Applications/MAMP/tmp/mysql/mysql.sock', user='root',
                  password='root', database='software_engineering')
    db.connect()
    project_id = db.execute_insert(query, values)
    db.close()
    return {"project_id": project_id, "api_key": api_key}


# Update project

class ProjectUpdate(BaseModel):
    api_key: str
    name: str
    selected_features_indexes: list[int] = []


@router.post("/api/projects/{project_id}/update")
def update_project(project_id, project: ProjectUpdate):
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
