from collections.abc import Iterable
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os


class Cidade(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    ativo = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return f'{self.nome} ({self.uf})'
    
    def save(self, *args, **kwargs) -> None:
        self.nome = self.nome.upper()

        # if not self.slugf:
        #     self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

# Atualiza automaticamente o campo slug antes de salvar o objeto
@receiver(pre_save, sender=Cidade)
def updete_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f'{instance.nome} {instance.uf}')


class Fidelidade(models.Model):
    TIPO_CLIENTE_CHOICES = [
        ('Corporativo', 'Corporativo'),
        ('Residencial', 'Residencial'),
        # Adicione outras opções conforme necessário
    ]
    
    id = models.AutoField(primary_key=True)
    quantidade_meses = models.IntegerField()
    tipo_cliente = models.CharField(max_length=11, choices=TIPO_CLIENTE_CHOICES)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.quantidade_meses} meses'
    
    def save(self, *args, **kwargs) -> None:
        self.tipo_cliente = self.tipo_cliente.upper()
        return super().save(*args, **kwargs)


class PlanoAbrangencia(models.Model):
    id = models.AutoField(primary_key=True)
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING, related_name='abrangencias_planos')
    plano = models.ForeignKey('Plano', models.DO_NOTHING, related_name='abrangencias_cidades')

    def __str__(self):
        return f'Abrangência do Plano ({self.id})'


class PlanoItensCombo(models.Model):
    id = models.AutoField(primary_key=True)
    plano = models.ForeignKey('Plano', models.DO_NOTHING, related_name='combos_planos')
    item = models.ForeignKey('Item', models.DO_NOTHING, related_name='combos_itens')

    def __str__(self):
        return f'{self.id}'

class AcordoManager(models.Manager):
    def por_plano(self, plano):
        return self.filter(plano=plano)


class Acordo(models.Model):
    id = models.AutoField(primary_key=True)
    plano = models.ForeignKey('Plano', models.DO_NOTHING, related_name='acordos_fidelidade')
    fidelidade = models.ForeignKey(Fidelidade, models.DO_NOTHING)
    valor = models.FloatField()
    sla = models.CharField(max_length=30, blank=True, null=True)
    padrao = models.BooleanField()
    ativo = models.BooleanField(default=True)
    objects = AcordoManager()

    def __str__(self):
        return f'Acordo ({self.id}) para {self.plano.nome} com Fidelidade de {self.fidelidade.quantidade_meses} meses'

    def save(self, *args, **kwargs) -> None:
        self.sla = self.sla.upper()
        return super().save(*args, **kwargs)


class PlanoManager(models.Manager):
    def por_abrangencia(self, cidade):
        return self.filter(abrangencia=cidade)


class Plano(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    valor = models.FloatField(null=True)
    ordem = models.IntegerField(unique=True, null=True)
    taxa_up = models.FloatField()
    taxa_down = models.FloatField()
    destacar_plano = models.BooleanField()
    text_destaque = models.CharField(max_length=20, blank=True, null=True)
    tipo_cliente = models.CharField(max_length=11)
    tipo_link = models.CharField(max_length=13)
    combo = models.BooleanField()
    icon = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    abrangencia = models.ManyToManyField(Cidade, through=PlanoAbrangencia)
    itens = models.ManyToManyField('Item', through=PlanoItensCombo)
    fidelidade = models.ManyToManyField(Fidelidade, through=Acordo, related_name='planos')

    objects = PlanoManager()

    class Meta:
        ordering = ['ordem']
        verbose_name_plural = "Planos"

    def __str__(self):
        return f'{self.nome}'

    def save(self, *args, **kwargs) -> None:
        
        # Padãonezação de dados
        self.nome = self.nome.upper()
        self.tipo_cliente = self.tipo_cliente.upper()
        self.tipo_link = self.tipo_link.upper()

        if self.text_destaque:
            self.text_destaque = self.text_destaque.capitalize()
        
        return super().save(*args, **kwargs)


class ItemManager(models.Manager):
    def por_plano(self, plano):
        return self.filter(plano=plano)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=25)
    scm = models.BooleanField()
    ordem = models.IntegerField(unique=True, null=True)
    icone = models.CharField(max_length=255, blank=True, null=True)
    detalhe = models.TextField(blank=True, null=True)
    link_externo = models.URLField(blank=True, null=True)
    ativo = models.BooleanField()
    objects = ItemManager()

    class Meta:
        ordering = ['ordem']
        verbose_name_plural = "Itens"

    def __str__(self):
        return f'{self.nome}'
    
    def save(self, *args, **kwargs) -> None:
        self.nome = self.nome.upper()
        
        super().save(*args, **kwargs)
