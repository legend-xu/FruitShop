from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from FruitGP2.models import FruitUser


class TokenFruitUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token=request.query_params.get("token")
            user=cache.get(token)
            if user:
                return user,token
        except Exception as e:
            print(e)