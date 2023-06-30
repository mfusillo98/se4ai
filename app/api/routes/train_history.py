from fastapi import APIRouter
from pydantic import BaseModel

from app.database.database import get_db
import app.api.repository.projects as projects_repository


router = APIRouter()


# Create project

class GetTrainHistoryRequests(BaseModel):
    api_key: str


@router.post("/api/projects/{project_id}/train-history")
def get_train_history(project_id, request: GetTrainHistoryRequests):
    db = get_db()

    project = projects_repository.get_project(project_id, request.api_key)
    if project is None:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_train_history WHERE project_id = %s"
    values = [project_id, ]
    trains = db.execute_select(query, values)

    if len(trains) == 0:
        return {"STATUS": "ERROR", "message": "Trains not found"}

    return {"STATUS": "OK", "images": trains}


class PullTrainHistoryRequests(BaseModel):
    api_key: str
    history_id: int


@router.post("/api/projects/{project_id}/train-history/pull")
def pull_training(project_id, request: PullTrainHistoryRequests):
    db = get_db()

    project = projects_repository.get_project(project_id, request.api_key)
    if project is None:
        return {"STATUS": "ERROR", "message": "Project not found"}

    query = "SELECT * FROM project_train_history WHERE project_id = %s AND history_id = %s"
    values = [project_id, request.history_id]
    train = db.execute_select(query, values)

    if len(train) == 0:
        return {"STATUS": "ERROR", "message": "Train not found"}

    rows_affected = db.execute_update(
        "UPDATE projects SET selected_features_indexes = %s, trained = 1 WHERE project_id = %s",
        [train[0]["selected_features_indexes"], project_id])

    if rows_affected is None:
        return {"STATUS": "ERROR", "message": "Update failed"}

    return {"STATUS": "OK", "message": "Pull executed"}
