from django import forms

from players.models import Player
from .models import Team


class TeamForm(forms.ModelForm):
    def __init__(self, coach, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coach = coach

    def save(self):
        obj = super().save(commit=False)
        obj.coach = self.coach
        obj.save()
        return obj

    class Meta:
        model = Team
        fields = ('name', 'gender', 'age')


class AddPlayersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelMultipleChoiceField(
            queryset=Player.objects.all(),
            widget=forms.CheckboxSelectMultiple())

    def clean(self):
        added_players_count = self.instance.players.count()
        allowed_count = 16 - added_players_count
        if len(self.cleaned_data['players']) > allowed_count:
            raise forms.ValidationError('Please select no more than {}'.format(allowed_count))
        return self.cleaned_data

    class Meta:
        model = Team
        fields = ('players', )
