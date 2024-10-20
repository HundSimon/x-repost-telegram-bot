import json
import urllib.parse

import e621py_wrapper as e621
import requests
from pixivpy3 import AppPixivAPI

from modules.utils import refresh_access_token


def downloader(url):
    """
    Determines the type of URL and calls the appropriate downloader function.
    """
    try:
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
    except Exception as e:
        raise Exception(f"Error in downloader: {e}")


def x_downloader(url):
    """
    Downloads images from x.com using the x.com API.
    """
    try:
        api_url = url.replace("https://x.com", "https://api.vxtwitter.com")

        response = requests.get(api_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {api_url}. Status code: {response.status_code}")

        data = response.json()

        username = data.get("user_name")
        media_urls = data.get("mediaURLs", [])
        media_list = [url + "?name=orig" for url in media_urls]

        return media_list, username
    except Exception as e:
        raise Exception(f"Error in x_downloader: {e}")


def pixiv_downloader(url):
    """
    Downloads images from Pixiv.net using the Pixiv API.
    """
    try:
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
        image_list = [item['image_urls']['original'].replace('i.pximg.net', 'i.pixiv.re') for item in illust_detail.meta_pages]
        if not image_list:
            # If no meta_pages, use the original image URL
            image_urls = illust_detail.image_urls
            best_quality_image = image_urls[list(image_urls.keys())[-1]].replace('i.pximg.net', 'i.pixiv.re')
            image_list.append(best_quality_image)
        else:
            pass

        # Extract username
        username = illust_detail.user.name

        return image_list, username
    except Exception as e:
        raise Exception(f"Error in pixiv_downloader: {e}")


def kemonosu_downloader(url):
    """
    Downloads images from Kemono.su using the Kemono.su API.
    """
    try:
        image_list = []

        parsed_url = urllib.parse.urlparse(url)
        path_components = parsed_url.path.strip('/').split('/')
        _service = path_components[0]
        _user_id = path_components[2]
        _post_id = path_components[4]

        post_api_url = f"https://kemono.su/api/v1/{_service}/user/{_user_id}/post/{_post_id}"
        post_response = requests.get(post_api_url)
        if post_response.status_code != 200:
            raise Exception(f"Failed to fetch data from {post_api_url}. Status code: {post_response.status_code}")

        post_data = post_response.json()
        image_list.append("https://kemono.su" + post_data['file']['path'])
        for attachment in post_data['attachments']:
            image_list.append("https://kemono.su" + attachment['path'])

        image_list = list(dict.fromkeys(image_list))

        # Get username
        user_api_url = f"https://kemono.su/api/v1/{_service}/user/{_user_id}/profile"
        user_response = requests.get(user_api_url)
        if user_response.status_code != 200:
            raise Exception(f"Failed to fetch data from {user_api_url}. Status code: {user_response.status_code}")

        user_data = user_response.json()
        username = user_data['name']

        return image_list, username
    except Exception as e:
        raise Exception(f"Error in kemonosu_downloader: {e}")


def e621_downloader(url):
    """
    Downloads images from e621.net using the e621 API.
    """
    try:
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
    except Exception as e:
        raise Exception(f"Error in e621_downloader: {e}")


if __name__ == "__main__":
    pass