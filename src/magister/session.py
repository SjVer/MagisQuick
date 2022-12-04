from datetime import datetime as dt

from .. import log
from ..user.models import EUser
from .requests import get
from .api import get_tenant_id
from .auth import refresh, authenticate, TokenSet
from .data import *

__all__ = [
	"UserInfo",
	"MagisterSession"
]

class MagisterSession:
	# user stuff
	user: EUser
	
	# api stuff
	tokenset: TokenSet
	session_id: int
	
	# cached info
	__authenticated: bool
	
	def __init__(self, user: EUser):
		self.user = user
		
		self.tokenset = None
		self.session_id = None

		self.__authenticated = False
		
	def __bool__(self):
		return self.__authenticated

	def __assert_authenticated(self, name):
		if not self.__authenticated:
			raise Exception(f"not authenticated ({name})")
	
	# authenticate with Magister and get an access token
	def authenticate(self):
		if not self.user.school_id and False:
			self.user.school_id = get_tenant_id(self.user.school)
			log.info(f"retreived school id ({self.user.school_id[:10]}...)")

		# try refreshing tokens
		try:
			assert self.user.refresh_token

			log.info("attempting to refresh tokens")
			log.debug(f"  refresh token: {self.user.refresh_token[:10]}...")

			self.tokenset = refresh(self.user.refresh_token)
			assert self.tokenset

		except Exception as e:
			log.debug(f"  could not refresh tokens ({e.__class__.__name__})")

			# refreshing failed, so full authentication
			self.tokenset = authenticate(
				self.user.school_id,
				self.user.username,
				self.user.password_text
			)

			if not self.tokenset:
				self.__authenticated = False
				return

			# get tenant (thanks sjoerd :))! )
			self.user.tenant = get(
				None, self.tokenset.access_token,
				"https://cors.sjoerd.dev/https://magister.net/.well-known/host-meta.json"
			).json()["links"][0]["href"].strip("https://").split('.', 1)[0]
			
			self.user.refresh_token = self.tokenset.refresh_token
			self.user.save()

		if self.tokenset:
			self.__authenticated = True
			log.info(f"session authenticated (tenant: {self.user.tenant})")

	# update ID's and email address
	def update_credentails(self):
		self.__assert_authenticated("update_credentials")
		log.info("updating credentials")
		
		# retreive session id and account id
		data = get(
			self.user.tenant, self.tokenset.access_token,
			f"https://{self.user.tenant}.magister.net/api/sessions/current",
		).json()
		
		self.session_id = data["id"]
		account_link = data["links"]["account"]["href"]

		# retreive email and student id
		data = get(
			self.user.tenant, self.tokenset.access_token,
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
			self.user.tenant, self.tokenset.access_token,
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
	def account_api_url(self) -> str:
		self.require_credentials()
		return str.format(
			"https://{}.magister.net/api/personen/{}/",
			self.user.tenant,
			self.user.student_id
		)
		
	# get appointments
	def get_appointments(self, start: dt, end: dt) -> List[AppointmentData]:
		self.__assert_authenticated("get_appointments")

		start = start.strftime("%Y-%m-%d")
		end = end.strftime("%Y-%m-%d")
		log.info(f"getting appointments from {start} to {end}")

		apps = get(
			self.user.tenant, self.tokenset.access_token,
			self.account_api_url() + f"afspraken?status=1&tot={end}&van={start}"
		).json()["Items"]

		for app in apps:
			app["InfoType"] = AppInfoType(app["InfoType"])

		return apps