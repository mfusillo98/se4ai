from app.database.database import get_db
from scipy.spatial import distance


def search(project_id, selected_features_indexes, image_url, image_features, max_results=10):
    db = get_db()
    db.autocommit = False

    # Looping over all images
    images = db.execute_select(
        "SELECT ft.image_id, ft.features, res.*, img.url FROM project_resource_images_selected_features ft "
        "JOIN project_resource_images img ON img.image_id = ft.image_id "
        "JOIN project_resources res ON res.resource_id = img.resource_id "
        "WHERE res.project_id = %s", [project_id])
    ranking = []
    for image in images:
        features = [float(x) for x in image['features'].split(",")]
        d = distance.cosine(features, image_features)
        result_object = {
                "distance": d,
                "resource": {
                    "resource_id": image["resource_id"],
                    "name": image["name"],
                    "external_resource_id": image["external_resource_id"],
                    "created_at": image["created_at"],
                    "updated_at": image["updated_at"],
                },
                "image_id": image["image_id"],
                "image_url": image["url"]
            }
        if len(ranking) < max_results:
            ranking.append(result_object)
            ranking = sorted(ranking, key=lambda r: r["distance"])  # Resorting ranking
        elif ranking[len(ranking) - 1]["distance"] > d:
            ranking[len(ranking) - 1] = result_object
            ranking = sorted(ranking, key=lambda r: r["distance"])  # Resorting ranking

    search_id = db.execute_insert(
        "INSERT INTO project_search_performance "
        "(project_id, image_url, selected_features_indexes, results_with_feature_selection)"
        "VALUES (%s, %s, %s, %s)",
        [project_id, image_url, selected_features_indexes, ','.join([str(x["resource"]["resource_id"]) for x in ranking])]
    )

    # searchWithoutFeatureSelection(project_id,image_features, search_id, max_results);

    return ranking


def searchWithoutFeatureSelection(project_id, image_features, search_id, max_results=10):
    db = get_db()
    db.autocommit = False

    # Looping over all images
    images = db.execute_select(
        "SELECT ft.image_id, ft.features, res.*, img.url FROM project_resource_images_raw_features ft "
        "JOIN project_resource_images img ON img.image_id = ft.image_id "
        "JOIN project_resources res ON res.resource_id = img.resource_id "
        "WHERE res.project_id = %s", [project_id])
    ranking = []
    for image in images:
        features = [float(x) for x in image['features'].split(",")]
        d = distance.cosine(features, image_features)
        result_object = {
                "distance": d,
                "resource": {
                    "resource_id": image["resource_id"],
                    "name": image["name"],
                    "external_resource_id": image["external_resource_id"],
                    "created_at": image["created_at"],
                    "updated_at": image["updated_at"],
                },
                "image_id": image["image_id"],
                "image_url": image["url"]
            }
        if len(ranking) < max_results:
            ranking.append(result_object)
            ranking = sorted(ranking, key=lambda r: r["distance"])  # Resorting ranking
        elif ranking[len(ranking) - 1]["distance"] > d:
            ranking[len(ranking) - 1] = result_object
            ranking = sorted(ranking, key=lambda r: r["distance"])  # Resorting ranking

    db.execute_update("UPDATE project_search_performance SET results_without_feature_selection = %s WHERE search_id = %s",
                      [
                          ','.join([str(x["resource"]["resource_id"]) for x in ranking]),
                          search_id
                      ])