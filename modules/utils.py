import urllib

import requests


def get_media_type(url):
    try:
        # Use a HEAD request to get the content type without downloading the entire file
        response = requests.head(url, allow_redirects=True)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch HEAD data from {url}. Status code: {response.status_code}")

        content_type = response.headers.get('Content-Type', '').lower()

        if 'image' in content_type:
            return "image"
        elif 'video' in content_type:
            return "video"
        else:
            return "unknown"
    except Exception as e:
        raise Exception(f"Error in get_media_type: {e}")


def convert_special_chars(text: str) -> str:
    try:
        _special_chars = {
            '_': '\\_',
            '*': '\\*',
            '[': '\\[',
            ']': '\\]',
            '(': '\\(',
            ')': '\\)',
            '~': '\\~',
            '`': '\\`',
            '>': '\\>',
            '#': '\\#',
            '+': '\\+',
            '-': '\\-',
            '=': '\\=',
            '|': '\\|',
            '{': '\\{',
            '}': '\\}',
            '.': '\\.',
            '!': '\\!'
        }
        for char, escaped_char in _special_chars.items():
            text = text.replace(char, escaped_char)
        return text
    except Exception as e:
        raise Exception(f"Error in convert_special_chars: {e}")


def extract_username(url):
    try:
        if url.startswith("https://pixiv.net/artworks/"):
            pass
        elif url.startswith("https://x.com/"):
            parsed_url = urllib.parse.urlparse(url)
            path_components = parsed_url.path.split('/')

            if len(path_components) > 1:
                username = path_components[1]
                return username
            else:
                return None
        else:
            return None
    except Exception as e:
        raise Exception(f"Error in extract_username: {e}")


def refresh_access_token(refresh_token):
    try:
        USER_AGENT = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"
        REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"
        LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
        AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"
        CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
        CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"

        response = requests.post(
            AUTH_TOKEN_URL,
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "refresh_token",
                "include_policy": "true",
                "refresh_token": refresh_token,
            },
            headers={"User-Agent": USER_AGENT},
        )

        if response.status_code != 200:
            raise Exception(f"Failed to refresh access token. Status code: {response.status_code}")

        return response.json()["access_token"]
    except Exception as e:
        raise Exception(f"Error in refresh_access_token: {e}")


if __name__ == "__main__":
    try:
        print(extract_username("https://x.com/username/status/123456789"))
    except Exception as e:
        print(f"Error in main: {e}")
