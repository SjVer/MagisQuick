from .. import logging
from ..user.models import EUser
from .requests import get
from .auth import authenticate

__all__ = [
    "UserInfo",
    "MagisterSession"
]

class MagisterSession:
    # user stuff
    user: EUser
    
    # api stuff
    access_token: str
    session_id: int
    person_id: int
    
    # cached info
    __authenticated: bool
    
    def __init__(self, user: EUser):
        self.user = user
        
        self.access_token = None
        self.session_id = None
        self.person_id = None

        self.__authenticated = False
        self.__userinfo = None
        
    def __bool__(self):
        return self.__authenticated

    def __assert_authenticated(self, name):
        if not self.__authenticated:
            raise Exception(f"not authenticated ({name})")
    
    def authenticate(self):
        auth = authenticate(
            self.user.tenant,
            self.user.username,
            self.user.password_text)
        if not auth: return
        
        self.__authenticated = True
        self.access_token = auth["access_token"]
        self.session_id = auth["session_id"]
        self.person_id = auth["person_id"]
    
    def update_userinfo(self):
        self.__assert_authenticated("update_userinfo")

        logging.info("retreiving user info")
        data = get(
            self.user.tenant, self.access_token,
            "https://accounts.magister.net/connect/userinfo",
        ).json()
        
        # data["preferred_username"]
        self.user.first_name = data["given_name"]
        self.user.last_name = data["family_name"]
        self.user.middle_name = data["middle_name"]
        self.user.school = data["tenant_name"]
        self.user.save()

        logging.debug(f"  first name: {self.user.first_name}")
        logging.debug(f"  middle name: {self.user.middle_name}")
        logging.debug(f"  last name: {self.user.last_name}")
        logging.debug(f"  school: {self.user.school}")