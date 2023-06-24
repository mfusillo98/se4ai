import shutil
import requests
import os
import imghdr


default_referer = 'ProductImageSync'
default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
debug = True
use_image_header_test = False


def get_abs_path(relative_path):
    return os.path.dirname(os.path.realpath(__file__)) + str(relative_path).replace("/", os.path.sep)


def get_mime_type(url):
    r = requests.head(url, headers={'referer': default_referer, 'User-Agent': default_user_agent}, verify=False)
    return r.headers['content-type']


def check_image_header(path):
    if imghdr.what(path) is None:
        return False
    return True


def delete_file(path):
    if path is not None and os.path.exists(path):
        os.remove(path)
    return True


def safe_image_download(url, destination_path):
    # Checking Mime/type
    valid_types = ("image/png", "image/gif", "image/tiff", "image/jpeg", "image/jpg", "image/bmp", "image/webp")
    mime_type = get_mime_type(url)
    if mime_type not in valid_types:
        if debug:
            print(f"> Mime type {mime_type}  not valid, skipping")
        return False

    extension = mime_type.split('/')[-1]

    # Dowloading image
    image_request = requests.get(url, verify=False, stream=True,
                                 headers={'referer': default_referer, 'User-Agent': default_user_agent})
    if image_request.status_code != 200:  # Download non riuscito, aumento l'offset per la prossima richiesta
        if debug:
            print(f"> Image download status code {image_request.status_code}, skipping")
        return False

    # Storing image
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    image_request.raw.decode_content = True
    tmp_image_path = f"{destination_path}/tmp_img.{extension}"
    with open(tmp_image_path, 'wb') as f:
        shutil.copyfileobj(image_request.raw, f)

    if not os.path.isfile(tmp_image_path):
        if debug:
            print(F"> Cannot save the image to disk, skipping")
        return False

    # Image file validity check
    if use_image_header_test and not check_image_header(tmp_image_path):
        if debug:
            print(F"> Imghdr test failed")
        # delete_file(tmp_image_path)
        # return False

    return tmp_image_path
