from django.http import HttpRequest
from .session import MagisterSession

__all__ = [
    "MagisterSession",
    "clear_session",
    "get_session",
]

__current_session: MagisterSession = None

def clear_session():
    global __current_session
    __current_session = None

def get_session(request: HttpRequest) -> MagisterSession:
    global __current_session
    # session: MagisterSession = request.user.session
    
    if not __current_session:
        __current_session = MagisterSession(request.user)
        __current_session.authenticate()
        # request.user.session = session
    
    return __current_session

# def get_grades(session: MagisterSession):
#     url = f"https://{session.school}.magister.net/api/personen/{session.id}/cijfers/laatste?top=25&skip=0"
#     r = requests.get(url, headers=header(session.school, session.token), timeout=5)
#     return r.json()
