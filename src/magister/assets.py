from requests import get as raw_get
from .. import log

def __get_content(url):
    try:
        return raw_get(url).content
    except Exception as e:
        log.error(f"failed to get webfont: {e.args[0]}")
        return None

def get_webfont(tenant: str):
    return __get_content(f"https://{tenant}.magister.net/magister/assets/fonts/magistersymbols-webfont.woff")
