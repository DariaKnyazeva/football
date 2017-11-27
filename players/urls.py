from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import RegistractionView, PlayerListView, PlayerCreateView, PlayerEditView


urlpatterns = [
    url(r'^registration/$', RegistractionView.as_view(), name='players_registration'),
    url(r'^registration_thanks/$', TemplateView.as_view(template_name='players_registration_thanks.html')),
    url(r'^list/$', login_required(PlayerListView.as_view()), name='player_list'),
    url(r'^add/$', login_required(PlayerCreateView.as_view()), name='add_player'),
    url(r'^(?P<player_id>\d+)/edit/$', login_required(PlayerEditView.as_view()), name='edit_player'),
]
