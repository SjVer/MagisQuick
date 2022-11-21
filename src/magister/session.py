from typing import TypedDict, List
from datetime import datetime as dt

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
		# try restoring last session
		if self.user.last_access_token:
			logging.info("attempting to restore session")
			logging.debug(f"  old access token: {self.user.last_access_token[:10]}...")

			status_code = get(
				self.user.tenant, self.user.last_access_token,
				f"https://{self.user.tenant}.magister.net/api/sessions/current"
			).status_code

			if status_code == 200:
				# code 200 means success
				self.access_token = self.user.last_access_token

		if not self.access_token:
			# restoring fialed, so full authentication
			self.access_token = authenticate(
				self.user.tenant,
				self.user.username,
				self.user.password_text
			)

			if not self.access_token:
				self.__authenticated = False
				return

			self.user.last_access_token = self.access_token
			self.user.save()

		self.__authenticated = True
		logging.info(f"session authenticated")

	# update ID's and email address
	def update_credentails(self):
		self.__assert_authenticated("update_credentials")
		logging.info("updating credentials")
		
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
	
	def require_credentials(self):
		if self.session_id: return
		else: self.update_credentails()
	
	# update user information
	def update_userinfo(self):
		self.__assert_authenticated("update_userinfo")
		logging.info("updating user info")

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
		
	def require_userinfo(self):
		if self.user.first_name: return
		else: self.update_userinfo()
	
	# {tenant}.magister.net/api/personen/{id}
	def account_api_url(self):
		self.require_credentials()
		return str.format(
			"https://{}.magister.net/api/personen/{}/",
			self.user.tenant,
			self.user.student_id
		)
		
	# get appointments
	def get_appointments(self, start: dt, end: dt):
		start = start.strftime("%Y-%m-%d")
		end = end.strftime("%Y-%m-%d")
		logging.info(f"getting appointments from {start} to {end}")

		class Data(TypedDict):
			Aantekeningen: dict # ?
			Afgerond: bool
			Bijlagen: list # ?
			Docenten: list # Docentencode: str, Naam: str
			DuurtHeleDag: bool
			Einde: str
			Id: int
			LesuurTotMet: int
			LesuurVan: int
			Lokatie: str
			Omschrijving: str
			Start: str
			Vakken: list # Naam: str

		data: List[Data] = get(
			self.user.tenant, self.access_token,
			self.account_api_url() + f"afspraken?van={start}&tot={end}"
		).json()["Items"]
  
		return data 