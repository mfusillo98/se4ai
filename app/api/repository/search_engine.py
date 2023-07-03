from app.database.database import get_db
from scipy.spatial import distance


def search(project_id, image_features, max_results=10):
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

    return ranking