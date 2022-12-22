from django.http import HttpRequest
from .session import MagisterSession

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