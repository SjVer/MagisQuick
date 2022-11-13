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
    
    # cached info
    __authenticated: bool
    
    def __init__(self, user: EUser):
        self.user = user
        
        self.access_token = None
        self.session_id = None

        self.__authenticated = False
        
    def __bool__(self):
        return self.__authenticated

    def __assert_authenticated(self, name):
        if not self.__authenticated:
            raise Exception(f"not authenticated ({name})")
    
    # authenticate with Magister and get an access token
    def authenticate(self):
        # authenticate
        access_token = authenticate(
            self.user.tenant,
            self.user.username,
            self.user.password_text
        )
        if not access_token: return

        self.__authenticated = True
        self.access_token = access_token
        self.update_credentails()

    # update ID's and email address
    def update_credentails(self):
        # retreive session id and account id
        data = get(
            self.user.tenant, self.access_token,
            f"https://{self.user.tenant}.magister.net/api/sessions/current",
        ).json()
        self.session_id = data["id"]
        account_link = data["links"]["account"]["href"]
        self.user.account_id = account_link.split("/")[-1]

        # retreive email and student id
        data = get(
            self.user.tenant, self.access_token,
            f"https://{self.user.tenant}.magister.net/api/accounts/{self.user.account_id}",
        ).json()
        self.user.email = data["emailadres"]
        student_link = data["links"]["leerling"]["href"]
        self.user.student_id = student_link.split("/")[-1]

        self.user.save()

        logging.debug(f"  session id: {self.session_id}")
        logging.debug(f"  account id: {self.user.account_id}")
        logging.debug(f"  student id: {self.user.student_id}")
        logging.debug(f"  email : {self.user.email}")
    
    # update user information
    def update_userinfo(self):
        self.__assert_authenticated("update_userinfo")

        logging.info("retreiving user info")
        userinfo = get(
            self.user.tenant, self.access_token,
            "https://accounts.magister.net/connect/userinfo",
        ).json()
        
        self.user.first_name = userinfo["given_name"]
        self.user.last_name = userinfo["family_name"]
        self.user.middle_name = userinfo["middle_name"]
        self.user.school = userinfo["tenant_name"]
        self.user.save()

        logging.debug(f"  first name: {self.user.first_name}")
        logging.debug(f"  middle name: {self.user.middle_name}")
        logging.debug(f"  last name: {self.user.last_name}")
        logging.debug(f"  school: {self.user.school}")