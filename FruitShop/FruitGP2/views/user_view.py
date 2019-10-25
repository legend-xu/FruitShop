from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from FruitGP2.models import FruitUser
from FruitGP2.serializers import FruitUserSerializer
from FruitGP2.tasks import send_activate_email_async
from FruitGP2.utils import generate_user_token, send_active_email
from FruitShop.settings import USER_TOKEN_TIMEOUT


class FruitUsersAPIView(viewsets.ModelViewSet):

    queryset = FruitUser.objects.filter(Q(is_delete=False) & Q(is_forbidden=False))
    serializer_class = FruitUserSerializer
    def handle_post(self, request, *args, **kwargs):

        action = request.query_params.get("action")

        if action == "register":
            return self.do_register(request)
        elif action == "login":
            return self.do_login(request)
        elif action == "check_user":
            return self.check_user(request)
        elif action == "check_email":
            return self.check_email(request)
        else:
            return self.handle_unknown_action(request)
    def do_register(self, request):
        response = self.create(request)

        data = {
            "status": status.HTTP_201_CREATED,
            "msg": "create success",
            "data": response.data
        }
        task_id=send_activate_email_async.delay(response.data.get("f_name"), response.data.get("f_email"))
        # send_active_email(response.data.get("f_name"), response.data.get("f_email"))
        print(task_id)
        return Response(data)

    def perform_create(self, serializer):
        # serializer.save(f_password=make_password(self.request.data.get("f_password")))
        serializer.save(f_password=self.request.data.get("f_password"))

    def do_login(self, request):
        f_name = request.data.get("f_name")
        f_password = request.data.get("f_password")

        users = FruitUser.objects.filter(f_name=f_name)
        if not users.exists():

            data = {
                "msg": "doesn't exists",
                "status": status.HTTP_404_NOT_FOUND
            }

            return Response(data)

        user = users.first()

        if not user.verify_password(f_password):

            data = {
                "msg": "password error",
                "status": status.HTTP_401_UNAUTHORIZED
            }

            return Response(data)

        token = generate_user_token()

        cache.set(token, user, USER_TOKEN_TIMEOUT)
        # a9f34052be8d42e890f3c576d27ce5da
        data = {
            "msg": "login success",
            "status": status.HTTP_200_OK,
            "token": token,
            "data": self.get_serializer(user).data
        }


        return Response(data)

    def check_user(self, request):
        f_name = request.data.get("f_name")

        if FruitUser.objects.filter(f_name=f_name).exists():

            data = {
                "msg": "user exists",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)

        data = {
            "msg": "ok",
            "status": status.HTTP_200_OK
        }

        return Response(data)

    def check_email(self, request):
        f_email = request.data.get("f_email")

        if FruitUser.objects.filter(f_email=f_email).exists():
            data = {
                "msg": "email exists",
                "status": status.HTTP_409_CONFLICT
            }

            return Response(data)

        data = {
            "msg": "ok",
            "status": status.HTTP_200_OK
        }

        return Response(data)


    def handle_unknown_action(self, request):
        data={
            "msg":"notfind",
            "status": status.HTTP_404_NOT_FOUND
        }
        return Response(data)
    def handle_get(self,request):
        action=request.query_params.get("action")
        if action == "activate":
            return self.do_action(request)
        else:
            return self.handle_unknown_action(request)

    def do_action(self,request):
        token=request.query_params.get("token")
        username=cache.get(token)
        print(username,token)
        if not username:
            data={
                "msg":"timeout",
                "status":status.HTTP_408_REQUEST_TIMEOUT
            }
            return Response(data)
        user=FruitUser.objects.filter(f_name=username)
        if not user.exists():
            data={
                "msg":"notfound",
                "status":status.HTTP_404_NOT_FOUND
            }
            return Response(data)

        user=FruitUser.objects.filter(f_name=username).first()
        if user.is_activite:
            data={
                "msg":"activate succeessful",
                "status":status.HTTP_200_OK
            }
            return Response(data)
        user.is_activite=True
        user.save()
        cache.delete(token)
        data={
            "msg":"successful activited",
            "status":status.HTTP_200_OK
        }
        return Response(data)