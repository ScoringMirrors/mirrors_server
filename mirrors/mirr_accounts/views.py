from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .utils import (create_check_image, validity_check_image, create_register_token, get_ip, validity_register_token)
from .models import UserProfile


class LoginView(APIView):
    """docstring for LoginView"""

    authentication_class = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny, )

    def get(self, request):
        content = [{
            'user': str(request.user),
            'auth': str(request.auth),
        }, ]
        return Response(content)

    def post(self, request):
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


class RegisterView(ViewSet):
    """docstring for RegisterView"""

    authentication_class = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny, )

    @staticmethod
    def check_user(query_params, check_key_list):
        for key in check_key_list:
            if query_params.get(key):
                if User.objects.filter(**{key: query_params.get(key)}).exists():
                    return Response(data=[{'result': 'faild',
                                           'msg': 'this {} is registered!'.format(key), 'code': 601}, ])

    def list(self, request):
        query_params = request.query_params
        response = self.check_user(query_params, ['email', 'mobile_no'])
        if response is None:
            return Response()
        return response

    def create(self, request):
        check_key_list = ['password', 'password2', 'email', 'nikename']
        query = request.data
        for key in check_key_list:
            if not query.get(key):
                return Response(data=[{'result': 'faild', 'msg': '{} is error'.format(key), 'code': 601}, ],
                                status=status.HTTP_400_BAD_REQUEST)

        if validity_register_token(get_ip(request), query.get('image_id'), query.get('register_token')) is False:
            return Response(data=[{'result': 'faild', 'msg': 'incorrect certification information!', 'code': 601}, ],
                            status=status.HTTP_400_BAD_REQUEST)

        if query['password'] != query['password2']:
            return Response(data=[{'result': 'faild', 'msg': 'two passwords are inconsistent!', 'code': 601}, ],
                            status=status.HTTP_400_BAD_REQUEST)

        response = self.check_user(query, ['email', ])
        if response is not None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response

        user = User.objects.create(username=query['email'], email=query['email'])
        user.set_password(query['password'])
        user.save()
        userprofile = UserProfile.objects.create(user=user,
                                                 nikename=query['nikename'],
                                                 mobile_no=query.get('mobile_no'),
                                                 gender=query.get('gender'))
        return Response(data=[{'result': 'successful', 'msg': '{} registration success'.format(userprofile.nikename),
                               'code': 600}, ],
                        status=status.HTTP_201_CREATED)


class CheckImageView(APIView):
    """docstring for CheckImageView"""

    authentication_class = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny, )

    def get(self, request):
        (image_id, image_value) = create_check_image(int(timezone.now().timestamp()))
        return Response(data=[{'result': {'key': image_id, 'value': image_value},
                               'msg': 'ok', 'code': 600}, ])

    def post(self, request):
        image = {
            'image_id': request.data.get('image_id'),
            'image_value': request.data.get('image_value'),
        }
        (_, is_pass) = validity_check_image(image['image_id'], image['image_value'])
        if is_pass:
            return Response(data=[{'result': create_register_token(get_ip(request), image['image_id']),
                                   'msg': 'ok', 'code': 600}, ])

        return Response(data=[{'result': 'image value is error!', 'msg': 'ok', 'code': 601}, ])
