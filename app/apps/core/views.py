# apps/plano/views.py
from django.shortcuts import render, redirect
from apps.planos.models import Cidade
from apps.planos.forms import SelectCityForm
from django.urls import reverse

def home(request):
    if request.method == 'POST':
        form = SelectCityForm(request.POST)
        if form.is_valid():
            cidade_slug = form.cleaned_data['cidade_slug'].slug
            return redirect(reverse('planos_by_city', args=[cidade_slug]))
    else:
        form = SelectCityForm()

    cities = Cidade.objects.all()
    return render(request, 'core/home.html', {'form': form, 'cities': cities})
