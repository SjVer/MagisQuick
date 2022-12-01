from django.contrib.auth import backends, get_user_model

from .magister import get_session
from . import log

UserModel = get_user_model()

class EBackend(backends.ModelBackend):

    def authenticate(self, request, school=None, username=None, password=None, **kwargs):
        if school is None: school = kwargs.get(UserModel.SCHOOL_FIELD)
        if username is None: username = kwargs.get(UserModel.USERNAME_FIELD)
        if school is None or username is None or password is None: return

        try:
            user = UserModel._default_manager.get_by_natural_key(username, school)
        except UserModel.DoesNotExist:
            user = UserModel._default_manager.create_user(school, username, password)

            # use get_session to check if the credentials
            # are also OK with magister and set the current
            # session if it is (so we don't need to auth
            # again as soon as we enter another page)
            class FakeRequest: pass
            r = FakeRequest()
            r.user = user
            try:
                assert get_session(r)
            except Exception:
                user.delete()
                return

            log.info(f"creating valid new user {username} ({school})")
        finally:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        
