from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import TeamListView, TeamCreateView, TeamEditView, TeamAddPlayersView


urlpatterns = [
    url(r'^list/$', login_required(TeamListView.as_view()), name='team_list'),
    url(r'^add/$', login_required(TeamCreateView.as_view()), name='add_team'),
    url(r'^(?P<team_id>\d+)/edit/$', login_required(TeamEditView.as_view()), name='edit_team'),
    url(r'^(?P<team_id>\d+)/add_players/$', login_required(TeamAddPlayersView.as_view()), name='add_team_players'),
]