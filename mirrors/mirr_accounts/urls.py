from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
# from rest_framework import routers
from django.contrib.auth.decorators import login_required

from .views import LoginView, LogoutView


# router = routers.DefaultRouter(trailing_slash=False)
urlpatterns = [
    url(r'^login/$', csrf_exempt(LoginView.as_view()), name='login'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout'),
]
