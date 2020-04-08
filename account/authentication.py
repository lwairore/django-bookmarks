"""
    Django allows you to authenticate against different sources. The `AUTHENTICATION_BACKENDS` setting includes the list of authentication backends for your project. By default, this setting is set as follows:
        `['django.contrib.auth.backends.ModelBackend']`

    The default ModelBackend authenticates users against the database using the user model of `django.contrib.auth`. This will suit most of your projects. However, you can create custom backends to authenticate your user against other sources, such as an LDAP directory or any other system.

    You can read more information about customizing authentication at https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#other-authentication-sources.

    Whenever you use the authenticate() function of django.contrib.auth, Django tries to authenticate the user against each of the backends defined in AUTHENTICATION_BACKENDS one by one, until one of them successfully authenticates the user. Only if all of the backends fail to authenticate will the user not be authenticated into your site.

    Django provides a simple way to define your own authentication backends. An authentication backend is a class that provides the following two methods:

        1. authenticate(): It takes the request object and user credentials as parameters. It has to return a user object that matches those credentials if the credentials are valid, or None otherwise. The request parameter is an HttpRequest object, or None if it's not provided to authenticate().
        2. get_user(): Takes a user ID parameter and has to return a user object.

"""

from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


"""
    The preceding code is a simple authentication backend. The authenticate() method receives a request object and the username and password optional parameters. We could use different parameters, but we use username and password to make our backend work with the authentication framework views straight away. The preceding code works as follows:
        1. authenticate(): We try to retrieve a user with the given email address and check the password using the built-in check_password() method of the user model. This method handles the password hashing to compare the given password against the password stored in the database.
        2. get_user(): We get a user through the ID set in the user_id parameter. Django uses the backend that authenticated the user to retrieve the User object for the duration of the user session.

    Edit the settings.py file of your project and add the following setting:
        `AUTHENTICATION_BACKENDS = [
            'django.contrib.auth.backends.ModelBackend',
            'account.authentication.EmailAuthBackend',
        ]`

    In the preceding setting, we kept the default ModelBackend that is used to authenticate with username and password and included our own email-based authentication backend. Now, open http://127.0.0.1:8000/account/login/ in your browser. Remember that Django will try to authenticate the user against each of the backends, so now we should be able to log in seamlessly using your username or email account. User credentials will be checked using the ModelBackend authentication backend, and if no user is returned, credentials will be checked using our custom EmailAuthBackend backend.

    The order of the backends listed in the AUTHENTICATION_BACKENDS setting matters. If the same credentials are valid for multiple backends, Django will stop at the first backend that successfully authenticates the user.
"""

