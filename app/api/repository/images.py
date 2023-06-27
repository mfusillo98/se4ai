from app.database.database import get_db
from app.feature_extraction.model import extract_features_from_url


def add_resource_image(resource_id, img_url, compute_features=True):
    """
    Add a new image and compute it's raw features if requested
    :param resource_id:
    :param img_url:
    :return: image_id
    """
    db = get_db()
    query = "INSERT INTO project_resource_images (url, resource_id) VALUES (%s, %s)"
    values = [img_url, resource_id]
    image_id = db.execute_insert(query, values)
    if image_id is None:
        return {"STATUS": "ERROR", "MESSAGE": "Image Store failed"}

    if compute_features:
        try:
            image_raw_features = extract_features_from_url(img_url)

            query = "INSERT INTO project_resource_images_raw_features (image_id, features) VALUES (%s, %s)"
            values = [image_id, ','.join([str(v) for v in image_raw_features])]
            image_id = db.execute_insert(query, values)
            if image_id is None:
                return {"STATUS": "ERROR", "MESSAGE": "Image Store failed"}
        except:
            return {"STATUS": "ERROR", "MESSAGE": "Image Store failed"}
    return image_id
