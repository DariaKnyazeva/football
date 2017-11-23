from django.conf.urls import url
from .views import signup_coach


urlpatterns = [
    url(r'^signup/$', signup_coach, name='signup_coach'),
]
