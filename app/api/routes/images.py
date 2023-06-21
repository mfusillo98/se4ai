import sqlite3

from fastapi import APIRouter

router = APIRouter()


# Get images

@router.get("/api/projects/{project_id}/resources/{external_id}/images")
def get_image(project_id, external_id):
    conn = sqlite3.connect('Database/app.db')
    return project_id


# Add image

@router.post("/api/projects/{project_id}/resources/{external_id}/images/add")
def add_image(project_id, external_id):
    return project_id


# delete image

@router.post("/api/projects/{project_id}/resources/{external_id}/images/delete")
def delete_image(project_id, external_id):
    return project_id
