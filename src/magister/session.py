from typing import TypedDict, List
from datetime import datetime as dt

from .. import log
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
		try:
			log.info("attempting to restore session")
			log.debug(f"  old access token: {self.user.last_access_token[:10]}...")

			# if this request fails it means that the token doesn't work
			# we have no use for the retreived data
			get(
				self.user.tenant, self.user.last_access_token,
				f"https://accounts.magister.net/connect/userinfo"
			)

			self.access_token = self.user.last_access_token

		except Exception as e:
			log.debug(f"  could not restore session (exception {e.__class__.__name__})")

			# restoring fialed, so full authentication
			self.access_token = authenticate(
				self.user.school,
				self.user.username,
				self.user.password_text
			)

			if not self.access_token:
				self.__authenticated = False
				return

			# get tenant (thanks sjoerd :))! )
			self.user.tenant = get(
				None, self.access_token,
				"https://cors.sjoerd.dev/https://magister.net/.well-known/host-meta.json"
			).json()["links"][0]["href"].strip("https://").split('.', 1)[0]
			
			self.user.last_access_token = self.access_token
			self.user.save()

		if self.access_token:
			self.__authenticated = True
			log.info(f"session authenticated (tenant: {self.user.tenant})")

	# update ID's and email address
	def update_credentails(self):
		self.__assert_authenticated("update_credentials")
		log.info("updating credentials")

		__import__("pprint").pprint(
			get(
				self.user.tenant, self.access_token,
				f"https://dewillem.magister.net/api/account"
			)
		)
		
		# retreive session id and account id
		data = get(
			self.user.tenant, self.access_token,
			f"https://{self.user.tenant}.magister.net/api/sessions/current",
		).json()
		
		self.session_id = data["id"]
		account_link = data["links"]["account"]["href"]
		# self.user.account_id = account_link.split("/")[-1]

		# retreive email and student id
		data = get(
			self.user.tenant, self.access_token,
			f"https://{self.user.tenant}.magister.net/{account_link}",
		).json()
		
		self.user.account_id = data["id"]
		self.user.email = data["emailadres"]
		student_link = data["links"]["leerling"]["href"]
		self.user.student_id = student_link.split("/")[-1]

		self.user.save()

		log.debug(f"  session id: {self.session_id}")
		log.debug(f"  account id: {self.user.account_id}")
		log.debug(f"  student id: {self.user.student_id}")
		log.debug(f"  email : {self.user.email}")
	
	def require_credentials(self):
		if None or "" in [
			# self.session_id,
			self.user.account_id,
			self.user.email,
			self.user.student_id
		]: self.update_credentails()
	
	# update user information
	def update_userinfo(self):
		self.__assert_authenticated("update_userinfo")
		log.info("updating user info")

		userinfo = get(
			self.user.tenant, self.access_token,
			"https://accounts.magister.net/connect/userinfo",
		).json()
		
		self.user.first_name = userinfo["given_name"]
		self.user.last_name = userinfo["family_name"]
		self.user.middle_name = userinfo["middle_name"]
		self.user.save()

		log.debug(f"  first name: {self.user.first_name}")
		log.debug(f"  middle name: {self.user.middle_name}")
		log.debug(f"  last name: {self.user.last_name}")
		
	def require_userinfo(self):
		if None or "" in [
			# self.session_id,
			self.user.first_name,
			self.user.last_name,
		]: self.update_userinfo()
	
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
		self.__assert_authenticated("get_appointments")

		start = start.strftime("%Y-%m-%d")
		end = end.strftime("%Y-%m-%d")

		end = "2022-12-04"
		start = "2022-11-27"
		log.info(f"getting appointments from {start} to {end}")

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
			self.account_api_url() + f"afspraken?status=1&tot={end}&van={start}"
		).json()["Items"]
  
		return data 