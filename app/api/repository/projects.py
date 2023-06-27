from app.database.database import get_db
from app.feature_selection.pca import get_best_features_indexes
import numpy as np


def get_project(project_id, api_key):
    db = get_db()
    query = "SELECT * FROM projects WHERE api_key = %s AND project_id = %s"
    values = [api_key, project_id]
    projectStored = db.execute_select(query, values)
    if len(projectStored) == 0:
        return None
    return projectStored


def train_project(project_id):
    db = get_db()

    # Getting best indexes
    rows = db.execute_select("SELECT raw.features FROM project_resource_images_raw_features raw "
                             "JOIN project_resource_images img ON img.image_id = raw.image_id "
                             "JOIN project_resources res ON res.resource_id = img.resource_id "
                             "WHERE res.project_id = %s", [project_id]);
    feature_list = []
    for r in rows[:]:
        feature_list.append([float(x) for x in r['features'].split(",")])
    best_features_indexes = get_best_features_indexes(np.array(feature_list))
    indexes_str = ','.join([str(idx) for idx in best_features_indexes])
    rows_affected = db.execute_update("UPDATE projects SET selected_features_indexes = %s WHERE project_id = %s",
                                      [indexes_str, project_id])
    if rows_affected is None:
        return {"STATUS": "ERROR", "message": "Update failed"}

    return {"STATUS": "ERROR", "message": "Project training completed"}


def apply_training(project):
    db = get_db()
    db.autocommit = False

    # Getting best indexes
    indexes = [int(x) for x in project["selected_features_indexes"].split(",")]

    # Looping over all images
    images = db.execute_select("SELECT raw.image_id, raw.features FROM project_resource_images_raw_features raw "
                               "JOIN project_resource_images img ON img.image_id = raw.image_id "
                               "JOIN project_resources res ON res.resource_id = img.resource_id "
                               "WHERE res.project_id = %s", [project["project_id"]])

    for image in images:
        raw_features = [float(x) for x in image['features'].split(",")]
        new_features = ','.join([str(raw_features[i]) for i in indexes])
        db.execute_delete("DELETE FROM project_resource_images_selected_features WHERE image_id = %s",
                          [image["image_id"]])
        id = db.execute_insert("INSERT INTO project_resource_images_selected_features (image_id, features) VALUES (%s, %s)",
                          [image["image_id"], new_features])
        if id is None:
            return {"STATUS": "ERROR", "MESSAGE": "Cannot store image's selected features"}

    db.conn.commit()
    return {"STATUS": "ERROR", "message": "Project training applied successfully"}
