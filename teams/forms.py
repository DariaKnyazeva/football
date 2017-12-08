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


class BaseAddPlayersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        added_ids = list(Team.objects.filter(players__isnull=False).values_list('players__id', flat=True))
        added_side_ids = list(Team.objects.filter(side_players__isnull=False).
                              values_list('side_players__id', flat=True))
        excluded_player_ids = set(added_ids + added_side_ids)

        if self.instance.gender == 'M':
            queryset = Player.objects.filter(salutation=Player.Salutation.MISTER)
        else:
            queryset = Player.objects.exclude(salutation=Player.Salutation.MISTER)
        self.fields[self.get_players_field_name()] = forms.ModelMultipleChoiceField(
            queryset=queryset.filter(age_group__id=self.instance.age.id).exclude(id__in=excluded_player_ids),
            widget=forms.CheckboxSelectMultiple(),
            required=False)

    def get_players_field_name(self):
        raise NotImplementedError()

    def get_max_players_count(self):
        raise NotImplementedError()

    def clean(self):
        added_players = list(getattr(self.instance, self.get_players_field_name()).
                             values_list('id', flat=True))
        allowed_count = self.get_max_players_count() - len(added_players)
        if len(self.cleaned_data.get(self.get_players_field_name(), [])) > allowed_count:
            raise forms.ValidationError('Please select no more than {}'.format(allowed_count))
        ids = list(self.cleaned_data[self.get_players_field_name()].values_list('id', flat=True)) + added_players
        self.cleaned_data[self.get_players_field_name()] = Player.objects.filter(id__in=ids)
        return self.cleaned_data

    class Meta:
        model = Team
        fields = ('players', )


class AddPlayersForm(BaseAddPlayersForm):
    def get_players_field_name(self):
        return 'players'

    def get_max_players_count(self):
        return 16

    class Meta:
        model = Team
        fields = ('players', )


class AddSidePlayersForm(forms.ModelForm):
    def get_players_field_name(self):
        return 'side_players'

    def get_max_players_count(self):
        return 11

    class Meta:
        model = Team
        fields = ('side_players', )
