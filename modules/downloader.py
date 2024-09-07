import json
import urllib
import requests
import re
from pixivpy3 import *
from .utils import *

def downloader(url):
    if url.startswith("https://x.com"):
        return x_downloader(url)
    elif url.startswith("https://www.pixiv.net"):
        return pixiv_downloader(url)

def x_downloader(url):
    image_dict = []
    fxtwitter_url = re.sub(r"x\.com", "d.fxtwitter.com", url)
    image_index = 1

    while True:
        image_url = fxtwitter_url + "/photo/" + str(image_index)
        response = requests.get(image_url)

        if response.status_code == 200:
            orig_image_url = response.url + "?name=orig"
            image_dict.append(orig_image_url)
            if orig_image_url == image_dict[0] and image_index > 1:
                image_dict.pop(-1)
                break
            image_index += 1
        else:
            break

    # Get username
    parsed_url = urllib.parse.urlparse(url)
    path_components = parsed_url.path.split('/')
    if len(path_components) > 1:
        username = path_components[1]

    username = convert_special_chars(username)
    return image_dict, username

def pixiv_downloader(url):
    image_dict = []
    with open('./config.json', 'r', encoding='utf-8') as configFile:
        config = json.load(configFile)
        config["PIXIV_ACCESS_TOKEN"] = refresh_access_token(config["PIXIV_REFRESH_TOKEN"])

    illust_id = url.split('/')[-1]
    api = AppPixivAPI()
    api.set_auth(access_token=config["PIXIV_ACCESS_TOKEN"], refresh_token=config["PIXIV_REFRESH_TOKEN"])
    image_urls = api.illust_detail(illust_id).illust.image_urls

    best_quality_image = image_urls[list(image_urls.keys())[-1]]
    image_dict.append(best_quality_image)

    # Get username
    username = api.illust_detail(illust_id).illust.user.name

    return image_dict, username

if __name__ == "__main__":
    pass
