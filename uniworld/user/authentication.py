from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from datetime import *

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        now = (datetime.utcnow()- timedelta(days=3))
        if token.created < now:
            raise AuthenticationFailed('Token has expired')

        return token.user, token
