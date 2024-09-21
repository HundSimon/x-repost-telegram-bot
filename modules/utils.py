import urllib
import requests


def get_media_type(url):
    # Use a HEAD request to get the content type without downloading the entire file
    response = requests.head(url)
    content_type = response.headers.get('Content-Type', '').lower()

    if 'image' in content_type:
        return "image"
    elif 'video' in content_type:
        return "video"
    else:
        return "unknown"


def convert_special_chars(text: str) -> str:
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


def extract_username(url):
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


def refresh_access_token(refresh_token):
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
    return response.json()["access_token"]


if __name__ == "__main__":
    print(extract_username())
