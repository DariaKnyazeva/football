from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import RegistractionView


urlpatterns = [
    url(r'^registration/$', RegistractionView.as_view(), name='players_registration'),
    url(r'^registration_thanks/$', TemplateView.as_view(template_name='players_registration_thanks.html')),
]