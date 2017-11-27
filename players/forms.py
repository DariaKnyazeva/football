from django import forms

from .models import Player, AgeGroup, FieldPosition


class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['age_group'] = forms.ModelMultipleChoiceField(
            queryset=AgeGroup.objects.all(),
            widget=forms.CheckboxSelectMultiple())
        self.fields['field_position'] = forms.ModelMultipleChoiceField(
            queryset=FieldPosition.objects.all(),
            widget=forms.CheckboxSelectMultiple(),
            label="Position")

    class Meta:
        model = Player
        fields = ('salutation', 'first_name', 'last_name', 'parent_first_name',
                  'parent_last_name', 'date_of_birth', 'email', 'age_group',
                  'field_position')
