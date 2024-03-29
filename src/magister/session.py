from datetime import datetime as dt

from .. import log
from ..user.models import EUser
from .requests import get
from .api import get_tenant_id
from .data import *
from . import auth

class NotAuthenticatedException(Exception): pass

class MagisterSession:
	# user stuff
	user: EUser
	
	# api stuff
	tokenset: auth.TokenSet
	session_id: int
	
	# cached info
	__authenticated: bool
	__grades: list
	__averages: dict
	__course_id: int
	
	def __init__(self, user: EUser):
		self.user = user
		
		self.tokenset = None
		self.session_id = None

		self.__authenticated = False
		self.__grades = None
		self.__course_id = None
		self.__averages = None
		
	def __bool__(self):
		return self.__authenticated

	def __assert_authenticated(self, name):
		if not self.__authenticated:
			raise NotAuthenticatedException(f"not authenticated ({name})")
	
	# authenticate with Magister and get an access token
	def authenticate(self):
		if not self.user.school_id:
			self.user.school_id = get_tenant_id(self.user.school)
			log.info(f"retreived school id ({self.user.school_id[:10]}...)")

		# try refreshing tokens
		try:
			assert self.user.refresh_token

			log.info("attempting to refresh tokens")
			log.debug(f"  refresh token: {self.user.refresh_token[:10]}...")

			self.tokenset = auth.refresh(self.user.refresh_token)
			assert self.tokenset

		except Exception as e:
			log.debug(f"  could not refresh tokens ({e.__class__.__name__})")

			# refreshing failed, so full authentication
			self.tokenset = auth.authenticate(
				self.user.school_id,
				self.user.username,
				self.user.password_text
			)

			if not self.tokenset:
				self.__authenticated = False
				return

			# we have no way of getting the tenant ourselves, but we can
			# bypass cors and get the tenant through the host link.
			# It's weird but it works.
			self.user.tenant = get(
				None, self.tokenset.access_token,
				"https://cors.sjoerd.dev/https://magister.net/.well-known/host-meta.json"
			).json()["links"][0]["href"].strip("https://").split('.', 1)[0]
			
			self.user.refresh_token = self.tokenset.refresh_token
			self.user.save()

		if self.tokenset:
			self.__authenticated = True
			log.info(f"session authenticated (tenant: {self.user.tenant})")

	def is_authenticated(self):
		return self.__authenticated

	def end_session(self):
		# notifies the magister server that 
		# this session is done
		auth.end_session(self.tokenset.id_token)
		self.__authenticated = False
		log.info("session ended")

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
	
	# just a handy function that returns the formatted
	# account url which is needed for e.g. appointments.
	# format: {tenant}.magister.net/api/personen/{account id}
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

		start = start.date()
		end = end.date()
		log.info(f"getting appointments from {start} to {end}")

		apps = get(
			self.user.tenant, self.tokenset.access_token,
			self.account_api_url() + f"afspraken?status=1&tot={end}&van={start}"
		).json()["Items"]

		for app in apps:
			app["InfoType"] = AppInfoType(app["InfoType"])

		return apps

	# get the current course id
	def get_course_id(self) -> int:
		self.__assert_authenticated("get_course_id")

		# return cached id if possible
		if self.__course_id:
			log.info(f"course id: {self.__course_id} (cached)")
			return self.__course_id

		date = dt.today().date()

		# get all courses
		courses = get(
			self.user.tenant, self.tokenset.access_token,
			self.account_api_url() + f"aanmeldingen/"
		).json()["Items"]

		# find current course (by date)
		# no need to check for no-matching-course
		for c in courses:
			start = c["Start"].split("T", 1)[0]
			end = c["Einde"].split("T", 1)[0]
			if start <= str(date) and str(date) <= end:
				self.__course_id = c["Id"]
				break

		log.info(f"course id: {self.__course_id}")
		return self.__course_id

	# get grades
	def get_grades(self) -> List[GradeData]:
		self.__assert_authenticated("get_grades")
		log.info(f"getting grades")

		# return cached grades if we have them
		if self.__grades:
			log.debug(f"  returning {len(self.__grades)} cached grades")
			return self.__grades
		
		course_id = self.get_course_id()
		
		# get the actual grades (all of them)
		grades = get(
			self.user.tenant, self.tokenset.access_token,
			self.account_api_url() + \
				f"aanmeldingen/{course_id}/cijfers/cijferoverzichtvooraanmelding"\
				"?actievePerioden=true&alleenBerekendeKolommen=false&alleenPTAKolommen=false"
		).json()["Items"]

		log.debug(f"  retreived {len(grades)} grades")
		self.__grades = grades
		return grades

	# gets all averages
	def get_averages(self) -> Dict[str, List[RelatedGradeData]]:
		self.__assert_authenticated("get_averages")
		log.info("getting averages")

		# return cached grades if we have them
		if self.__averages:
			log.debug(f"  returning {len(self.__averages)} cached averages")
			return self.__averages

		averages = {}
		for g in self.get_grades():
			if g["CijferKolom"]["KolomSoort"] != 2: continue
			id = g["CijferKolom"]["Id"]
			
			related = get(
				self.user.tenant, self.tokenset.access_token,
				self.account_api_url() + f"cijfers/gerelateerdekolommen/{id}"
			).json()["Items"]

			if not related: continue

			subject = related[0]["CVak"]
			if not subject in averages.keys(): averages[subject] = []
			averages[subject] += related

		log.debug(f"  retreived averages for {len(averages)} subjects")
		self.__averages = averages
		return averages