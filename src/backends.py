from django.contrib.auth import backends, get_user_model

from . import log

UserModel = get_user_model()

class SchoolAndEmailBackend(backends.ModelBackend):

    def authenticate(self, request, school=None, username=None, password=None, **kwargs):
        if school is None: school = kwargs.get(UserModel.TENANT_FIELD)
        if username is None: username = kwargs.get(UserModel.USERNAME_FIELD)
        if school is None or username is None or password is None: return

        try:
            user = UserModel._default_manager.get_by_natural_key(school, username)
        except UserModel.DoesNotExist:
            log.info(f"creating new user {username} ({school})")
            user = UserModel._default_manager.create_user(school, username, password)
        finally:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        
