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
            results_html.append(f"""
            <tr>
                <td>
                    <img src={r["image_url"]} style="max-height: 250px;"/>
                </td>
                <td>
                    {r["resource"]["name"]}
                </td>
                <td>
                    Distance {r["distance"]}
                </td>
            </tr>
            """)
        return HTMLResponse(content=f"""
            <html>
            <head>
                <title>Search results</title>
            </head>
            <body>
                <h1>Query image</h1>
                <img src={image_url} style="max-height: 250px;"/>
                
                <h2>Search results</h2>
                <table>
                    {''.join(results_html)}
                </table>
                
                <h1>Search again</h1>
                <form action="/api/projects/search" method="GET">
                    <input type="text" name="project_id" value="{project_id}" placeholder="Project ID"/>
                    <input type="text" name="api_key" value="{api_key}" placeholder="API Key" /><br/>
                    <input type="hidden" name="limit" value="{limit}"/>
                    <input type="hidden" name="html" value="{html}"/>
                    <input type="url" name="image_url" placeholder="Query Image URL" value="{image_url}" />
                    <button>Search</button>
                </form>
            </body>
            </html>
            """, status_code=200)
    else:
        return {"STATUS": "OK", "results": results}


@router.get("/")
def search_page():
    return HTMLResponse(content=f"""
                <html>
                <head>
                    <title>Search results</title>
                </head>
                <body>
                    <h1>Search in project</h1>
                    <form action="/api/projects/search" method="GET">
                        <input type="text" name="project_id" placeholder="Project ID"/>
                        <input type="text" name="api_key" placeholder="API Key" /><br/>
                        <input type="hidden" name="limit" value="10"/>
                        <input type="hidden" name="html" value="1"/>
                        <input type="url" name="image_url" placeholder="Query Image URL" />
                        <button>Search</button>
                    </form>
                </body>
                </html>
                """, status_code=200)