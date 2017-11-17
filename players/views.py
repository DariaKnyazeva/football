from django.views.generic.edit import FormView

from .forms import RegistractionForm


class RegistractionView(FormView):
    template_name = 'players_registration.html'
    form_class = RegistractionForm
    success_url = '/'

    def form_valid(self, form):

        # TODO: form.send_email()
        return super().form_valid(form)
