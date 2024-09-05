import urllib
import requests
import re

def downloader(url):
    if url.startswith("https://x.com"):
        return x_downloader(url)
    elif url.startswith("https://pixiv.net"):
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

    return image_dict

def pixiv_downloader(url):
    pass

def extract_username(url):
    parsed_url = urllib.parse.urlparse(url)

    # Split the path into components
    path_components = parsed_url.path.split('/')

    # The username should be the second component in the path
    if len(path_components) > 1:
        username = path_components[1]
        return username
    else:
        return None

if __name__ == "__main__":
    pass
