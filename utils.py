import random
import string
from urllib.parse import urlparse

from db import get_link_by_code


def normalize_url(url: str) -> str:
    url = url.strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(chars, k=length))
        if get_link_by_code(code) is None:
            return code


def build_short_url(base_url: str, short_code: str) -> str:
    return f"{base_url.rstrip('/')}/?code={short_code}"
