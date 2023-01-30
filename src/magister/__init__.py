from django.http import HttpRequest, FileResponse
from django.core.files.temp import gettempdir

from pathlib import Path
from os.path import exists, dirname

from .session import MagisterSession
from .requests import get
from .. import log

__current_session: MagisterSession = None

def clear_session():
    global __current_session
    __current_session = None

def get_session(request: HttpRequest) -> MagisterSession:
    global __current_session
    
    if not __current_session:
        __current_session = MagisterSession(request.user)
        __current_session.authenticate()
    
    return __current_session

def set_current_session(session: MagisterSession):
    global __current_session
    __current_session = session

def profile_img(request: HttpRequest):
    session = get_session(request)
    session.require_credentials()

    tenant, student_id = session.user.tenant, session.user.student_id
    img_file = Path(gettempdir(), "img", f"profile-{tenant}-{student_id}.jpeg")

    if not exists(img_file):
        # request new image
        log.info(f"requesting profile image ({tenant}, {student_id})")
        img_resp = get(
            tenant, session.tokenset.access_token,
            f"https://{tenant}.magister.net/api/leerlingen/{student_id}/foto?redirect_type=body"
        )
        img_resp.raise_for_status()

        log.debug(f"  saving profile image to {img_file}")
        Path(gettempdir(), "img").mkdir()
        file = open(img_file, "wb")
        file.write(img_resp.content)
        file.close()

    return FileResponse(open(img_file, "rb"))