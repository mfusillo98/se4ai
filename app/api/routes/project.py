import json
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.database.database import get_db
import random
import string
import app.api.repository.projects as projects_repository
import app.api.repository.search_engine as search_engine
from app.feature_extraction.model import extract_features_from_url
from utils import files

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

@router.get("/api/projects/search")
def search_project(api_key, project_id, image_url, limit, html):
    project = projects_repository.get_project(project_id, api_key)
    image_raw_features = extract_features_from_url(image_url)
    best_features_indexes = [int(x) for x in project["selected_features_indexes"].split(",")]
    image_features = [image_raw_features[i] for i in best_features_indexes]
    results = search_engine.search(project_id, image_features, int(limit))
    if html == "1":
        results_html = []
        for r in results:
            results_html.append(get_search_result_html(r))
        html_file = files.get_abs_path("/../pages/search-result-page.html")
        with open(html_file, 'r') as file:
            html_content = file.read()
            html_content = html_content.replace("{{query_image_url}}", image_url)
            html_content = html_content.replace("{{project_id}}", project_id)
            html_content = html_content.replace("{{api_key}}", api_key)
            html_content = html_content.replace("{{limit}}", limit)
            html_content = html_content.replace("{{html}}", html)
            html_content = html_content.replace("{{results}}", ''.join(results_html))
            return HTMLResponse(content=html_content, status_code=200)
    else:
        return {"STATUS": "OK", "results": results}


@router.get("/")
def search_page():
    html_content = files.get_abs_path("/../pages/search.html")
    with open(html_content, 'r') as file:
        data = file.read()
        return HTMLResponse(content=data, status_code=200)


def get_search_result_html(r):
    html_file = files.get_abs_path("/../pages/search-result-row.html")
    with open(html_file, 'r') as file:
        data = file.read()
        data = data.replace("{{image_url}}", r["image_url"])
        data = data.replace("{{name}}", r["resource"]["name"])
        data = data.replace("{{distance}}", str(r["distance"]))
        return data
