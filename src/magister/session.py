from typing import TypedDict
from dataclasses import dataclass

from .requests import get
from .auth import authenticate

__all__ = [
    "UserInfo",
    "MagisterSession"
]

class UserInfo(TypedDict):
    preferred_username: str
    given_name: str
    family_name: str
    middle_name: str
    email: str
    tenant_name: str

class MagisterSession:
    # api stuff
    tenant: str
    username: str
    access_token: str
    session_id: int
    person_id: int
    
    # cached info
    __authenticated: bool
    __userinfo: UserInfo
    
    def __init__(self):
        self.tenant = None
        self.username = None
        self.access_token = None
        self.session_id = None
        self.person_id = None
        self.__authenticated = False

    def __assert_authenticated(self, name):
        if not self.__authenticated:
            raise Exception(f"not authenticated ({name})")
    
    def authenticate(self, school, username, passwd):
        auth = authenticate(school, username, passwd)
        if not auth: return False
        
        self.__authenticated = True
        self.tenant = auth["tenant"]
        self.username = auth["username"]
        self.access_token = auth["access_token"]
        self.session_id = auth["session_id"]
        self.person_id = auth["person_id"]
    
    def get_userinfo(self):
        self.__assert_authenticated("get_userinfo")

        if not self.__userinfo:
            self.__userinfo = get(
                self.tenant, self.access_token,
                "https://accounts.magister.net/connect/userinfo",
            ).json()
        
        return self.__userinfo