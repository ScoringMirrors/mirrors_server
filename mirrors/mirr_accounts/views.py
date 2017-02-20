from django.contrib import auth
from django.contrib.auth import authenticate

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    """docstring for LoginView"""

    authentication_class = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        content = [{
            'user': str(request.user),
            'auth': str(request.auth),
        }, ]
        return Response(content)

    def post(self, request, format=None):
        user = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
        }
        user = authenticate(**user)
        if user is None:
            return Response(data=[{'result': 'faild', 'msg': 'username or password is error!', 'code': 601}, ])
        if user.is_active is False:
            return Response(data={'result': 'faild', 'msg': 'user is disabled!', 'code': 602})
        auth.login(request, user)
        return Response(data=[{'result': 'login', 'msg': 'ok', 'code': 600}, ])


class LogoutView(APIView):
    """docstring for LogoutView"""

    authentication_class = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        auth.logout(request)
        return Response(data=[{'result': 'logout', 'msg': 'ok', 'code': 600}, ])
