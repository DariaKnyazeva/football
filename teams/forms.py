from django import forms

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
