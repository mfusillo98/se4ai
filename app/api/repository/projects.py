from app.database.database import get_db
from app.feature_selection.pca import get_best_features_indexes
import numpy as np


def train_project(project_id):
    db = get_db()
    rows = db.execute_select(
        "SELECT raw.features FROM project_resource_images_raw_features raw JOIN project_resource_images img ON img.image_id = raw.image_id JOIN project_resources res ON res.resource_id = img.resource_id WHERE res.project_id = " + project_id);
    feature_list = []
    for r in rows[:]:
        feature_list.append([float(x) for x in r['features'].split(",")])
    print(get_best_features_indexes(np.array(feature_list)))
