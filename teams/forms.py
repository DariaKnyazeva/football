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
        added_ids = self.instance.players.all().values_list('id', flat=True)
        if self.instance.gender == 'M':
            queryset = Player.objects.filter(salutation=Player.Salutation.MISTER)
        else:
            queryset = Player.objects.exclude(salutation=Player.Salutation.MISTER)
        self.fields['players'] = forms.ModelMultipleChoiceField(
            queryset=queryset.filter(age_group__id=self.instance.age.id).exclude(id__in=added_ids),
            widget=forms.CheckboxSelectMultiple(),
            required=False)

    def clean(self):
        added_players = list(self.instance.players.values_list('id', flat=True))
        allowed_count = 16 - len(added_players)
        if len(self.cleaned_data.get('players', [])) > allowed_count:
            raise forms.ValidationError('Please select no more than {}'.format(allowed_count))
        ids = list(self.cleaned_data['players'].values_list('id', flat=True)) + added_players
        self.cleaned_data['players'] = Player.objects.filter(id__in=ids)
        return self.cleaned_data

    class Meta:
        model = Team
        fields = ('players', )
