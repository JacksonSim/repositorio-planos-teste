# apps/plano/forms.py
from django import forms
from .models import Cidade

class SelectCityForm(forms.Form):
    cidade_slug = forms.ModelChoiceField(
        queryset=Cidade.objects.filter(ativo=True),
        empty_label="Escolha a cidade",
        label="Cidade",
        widget=forms.Select(attrs={'class': 'form-select mb-3'}),
        to_field_name='slug'
    )
