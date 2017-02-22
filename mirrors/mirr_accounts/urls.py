from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import routers

from .views import LoginView, LogoutView, CheckImageView, RegisterView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'register', RegisterView, base_name='register')

urlpatterns = router.urls + [
    url(r'^login/$', csrf_exempt(LoginView.as_view()), name='login'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout'),
    url(r'^get_check_code/$', csrf_exempt(CheckImageView.as_view()), name='get_check_code'),
]
