import re
import json
import requests
import urllib.parse
from pixivpy3 import AppPixivAPI
from modules.utils import convert_special_chars, refresh_access_token
import e621py_wrapper as e621


def downloader(url):
    """
    Determines the type of URL and calls the appropriate downloader function.
    """
    if url.startswith("https://x.com"):
        return x_downloader(url)
    elif url.startswith("https://www.pixiv.net"):
        return pixiv_downloader(url)
    elif url.startswith("https://kemono.su"):
        return kemonosu_downloader(url)
    elif url.startswith("https://e621.net"):
        return e621_downloader(url)
    else:
        raise ValueError("Unsupported URL")


def x_downloader(url):
    """
    Downloads images from x.com using the fxtwitter.com mirror.
    """
    image_list = []
    fxtwitter_url = re.sub(r"x\.com", "d.fxtwitter.com", url)
    image_index = 1

    while True:
        image_url = f"{fxtwitter_url}/photo/{image_index}"
        response = requests.get(image_url)

        if response.status_code == 200:
            orig_image_url = f"{response.url}?name=orig"
            image_list.append(orig_image_url)

            # Break the loop if the same image URL repeats (to avoid duplicates) TODO: Better way to handle this?
            if orig_image_url == image_list[0] and image_index > 1:
                image_list.pop()
                break
            image_index += 1
        else:
            break

    # Extract username from URL
    parsed_url = urllib.parse.urlparse(url)
    path_components = parsed_url.path.split('/')
    username = convert_special_chars(path_components[1]) if len(path_components) > 1 else "Unknown"

    return image_list, username


def pixiv_downloader(url):
    """
    Downloads images from Pixiv.net using the Pixiv API.
    """
    image_list = []

    # Load configuration and refresh access token
    with open('./config.json', 'r', encoding='utf-8') as configFile:
        config = json.load(configFile)
        config["PIXIV_ACCESS_TOKEN"] = refresh_access_token(config["PIXIV_REFRESH_TOKEN"])

    illust_id = url.split('/')[-1]
    api = AppPixivAPI()
    api.set_auth(
        access_token=config["PIXIV_ACCESS_TOKEN"],
        refresh_token=config["PIXIV_REFRESH_TOKEN"]
    )

    # Fetch image URLs and select the best quality image
    illust_detail = api.illust_detail(illust_id).illust
    image_list = [item['image_urls']['original'] for item in illust_detail.meta_pages]
    if not image_list:
        # If no meta_pages, use the original image URL
        image_urls = illust_detail.image_urls
        best_quality_image = image_urls[list(image_urls.keys())[-1]]
        image_list.append(best_quality_image)
    else:
        pass


    # Extract username
    username = illust_detail.user.name

    return image_list, username

def kemonosu_downloader(url):
    """
    Downloads images from Kemono.su using the Kemono.su API.
    """
    image_list = []

    parsed_url = urllib.parse.urlparse(url)
    path_components = parsed_url.path.strip('/').split('/')
    _service = path_components[0]
    _user_id = path_components[2]
    _post_id = path_components[4]

    post_api_url = f"https://kemono.su/api/v1/{_service}/user/{_user_id}/post/{_post_id}"
    post_response = requests.get(post_api_url)
    post_data = post_response.json()
    image_list.append("https://kemono.su" + post_data['file']['path'])
    for attachment in post_data['attachments']:
        image_list.append("https://kemono.su" + attachment['path'])

    # Get username
    user_api_url = f"https://kemono.su/api/v1/{_service}/user/{_user_id}/profile"
    user_response = requests.get(user_api_url)
    user_data = user_response.json()
    username = user_data['name']

    return image_list, username

def e621_downloader(url):
    """
    Downloads images from e621.net using the e621 API.
    """
    image_list = []

    client = e621.client()

    parsed_url = urllib.parse.urlparse(url)
    path_components = parsed_url.path.strip('/').split('/')
    _image_type = path_components[0]
    image_id = path_components[1]

    if _image_type == "posts":
        image_url = client.posts.get(image_id)[0]["file"]["url"]
        image_list.append(image_url)
    elif _image_type == "pools":
        image_ids = client.pools.get(image_id)[0]["post_ids"]
        for image_id in image_ids:
            image_link = client.posts.get(image_id)[0]["file"]["url"]
            image_list.append(image_link)
    else:
        raise ValueError("Unsupported e621 URL")

    # Get username
    username = client.posts.get(image_id)[0]["tags"]["artist"][0]

    return image_list, username

if __name__ == "__main__":
    pass