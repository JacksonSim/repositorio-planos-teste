from django.shortcuts import render, get_object_or_404
from .models import Cidade, Plano, Acordo, Item, Fidelidade


def formata_valor(valor: float):
    novo_valor = str(valor).replace('.', ',')
    return f"{novo_valor}"


def planos_by_city(request, slug):
    city = get_object_or_404(Cidade, slug=slug)

    # Use select_related ou prefetch_related para otimizar consultas
    planos = Plano.objects.por_abrangencia(city)

    for plano in planos:
        plano.acordos = Acordo.objects.por_plano(plano)

        for acordo in plano.acordos:
            acordo.economia = (plano.valor * acordo.fidelidade.quantidade_meses) - \
                (acordo.valor * acordo.fidelidade.quantidade_meses)

            if acordo.padrao:
                plano.acor_padrao = acordo
                ...
            ...
        ...

    return render(
        request, 'planos/planos_by_city.html', {'city': city, 'planos': planos}
    )
