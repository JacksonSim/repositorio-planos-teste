from typing import Any
from django.http import HttpResponseNotFound
from django.urls import reverse
from dotenv import load_dotenv
load_dotenv()
import os

class AdminWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Adicione os IPs que podem acessar o painel de administração
        self.admin_allowed_ips = os.environ.get('ADMIN_WHITELIST').split(', ')
        ...


    def __call__(self, request):
        # Obtenha o endereço IP do cliente
        ip_address = request.META.get('REMOTE_ADDR')

        # Verifique se a solicitação é para o painel de administração
        if request.path.startswith(reverse('admin:index')):
            # Verifique se o IP está na lista de IPs permitidos para o admin
            if ip_address not in self.admin_allowed_ips:
                return HttpResponseNotFound('Não encontrado')

        # Continue o fluxo normal
        response = self.get_response(request)
        return response


class IPFilterMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        # Adiciona os IPs que podem acessaro site
        self.allowed_ips = os.environ.get('FULL_WHITELIST').split(', ')
        ...

    def __call__(self, request) -> Any:
        # Obtenha o ip do cliente que pode acessar o site
        ip_address = request.META.get('REMOTE_ADDR')
        # Verifica se o ip está na lista dos ips permitidos
        if ip_address not in self.allowed_ips:
            return HttpResponseNotFound('Não encontrado.')
            ...
        
        # Continue o fluxo normal se o ip estiver na lista de ips permitidos
        response = self.get_response(request)
        return response
