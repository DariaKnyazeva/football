from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView

from players.views import CoachViewMixin

from .forms import TeamForm, AddPlayersForm
from .models import Team


class TeamListView(CoachViewMixin, ListView):
    model = Team
    template_name = 'team_list.html'
    paginate_by = settings.RESULTS_PER_PAGE

    def get_queryset(self):
        return Team.objects.filter(coach=self.request.user)


class TeamCreateView(CoachViewMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'base/form_page.html'

    def get_success_url(self):
        return reverse('team_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add Team"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'coach': self.request.user})
        return kwargs

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Team has been created.')
        return HttpResponseRedirect(self.get_success_url())


class TeamEditView(CoachViewMixin, UpdateView):
    model = Team
    pk_url_kwarg = 'team_id'
    form_class = TeamForm
    template_name = 'team_edit.html'

    def get_success_url(self):
        return reverse('team_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context['title'] = "Edit Team"
        context['players'] = team.players.all()
        context['side_players'] = team.side_players.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'coach': self.request.user})
        return kwargs

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Team has been updated.')
        return HttpResponseRedirect(self.get_success_url())


class TeamAddPlayersView(CoachViewMixin, UpdateView):
    model = Team
    pk_url_kwarg = 'team_id'
    form_class = AddPlayersForm
    template_name = 'team_add_players.html'

    def get_success_url(self):
        return reverse('edit_team', kwargs={'team_id': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add Team Players"
        context['allowed_count'] = 16 - self.get_object().players.all().count()
        return context
