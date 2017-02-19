from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^login/$'),

]
