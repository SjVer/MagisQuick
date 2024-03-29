from django.contrib.auth import backends, get_user_model

from .magister import MagisterSession, set_current_session
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
            user.save()

            # check if the credentials are also OK with
            # magister and set the current session if
            # it is (so we don't need to auth again as
            # soon as we enter another page)
            try:
                log.info("checking new user authentication")
                session = MagisterSession(user)
                session.authenticate()
                assert session.is_authenticated()
                set_current_session(session)
            except Exception as e:
                log.info("authentication failed, deleting new user")
                log.debug(f"  {e}")
                user.delete()
                user = None
                return

            log.info(f"created valid new user {username} ({school})")
        finally:
            if not user is None and user.check_password(password) and self.user_can_authenticate(user):
                return user
        
    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None