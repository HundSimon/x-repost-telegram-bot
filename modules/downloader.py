import re
import json
import requests
import urllib.parse
from pixivpy3 import AppPixivAPI
from .utils import convert_special_chars, refresh_access_token


def downloader(url):
    """
    Determines the type of URL and calls the appropriate downloader function.
    """
    if url.startswith("https://x.com"):
        return x_downloader(url)
    elif url.startswith("https://www.pixiv.net"):
        return pixiv_downloader(url)
    else:
        raise ValueError("Unsupported URL")


def x_downloader(url):
    """
    Downloads images from x.com using the fxtwitter mirror.
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
    Downloads images from Pixiv using the Pixiv API.
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
    image_urls = illust_detail.image_urls
    best_quality_image = image_urls[list(image_urls.keys())[-1]]

    image_list.append(best_quality_image)

    # Extract username
    username = illust_detail.user.name

    return image_list, username


if __name__ == "__main__":
    pass
