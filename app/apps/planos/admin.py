from django.contrib import admin
from .models import Cidade, Fidelidade, PlanoAbrangencia, PlanoItensCombo, Acordo, Plano, Item

class PlanoAbrangenciaInline(admin.TabularInline):
    model = PlanoAbrangencia
    extra = 1


class PlanoItensComboInline(admin.TabularInline):
    model = PlanoItensCombo
    extra = 1

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'valor', 'ordem', 'taxa_up', 'taxa_down', 'destacar_plano', 'text_destaque', 'tipo_cliente', 'tipo_link', 'combo', 'icon', 'ativo']
    # filter_horizontal = ('itens', 'fidelidade')
    list_display_links = ['id', 'nome']
    inlines = [PlanoItensComboInline, PlanoAbrangenciaInline]
    list_filter = ['tipo_cliente', 'ativo']
    search_fields = ['nome']

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'uf', 'ativo']

@admin.register(Fidelidade)
class FidelidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantidade_meses', 'tipo_cliente', 'ativo']

@admin.register(PlanoAbrangencia)
class PlanoAbrangenciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cidade', 'plano']
    list_display_links = ['id', 'cidade']
    search_fields = ['cidade__nome', 'plano__nome']

@admin.register(PlanoItensCombo)
class PlanoItensComboAdmin(admin.ModelAdmin):
    list_display = ['id', 'plano', 'item']
    list_display_links = ['id', 'plano']
    search_fields = ['plano__nome', 'item__nome']

@admin.register(Acordo)
class AcordoAdmin(admin.ModelAdmin):
    list_display = ['id', 'plano', 'fidelidade', 'valor', 'sla', 'padrao', 'ativo']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'scm', 'ordem', 'icone', 'detalhe', 'link_externo', 'ativo']
