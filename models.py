# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Categoria(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Categoria'


class Perdidos(models.Model):
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    coordenada = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='categoria', blank=True, null=True)
    dni = models.CharField(max_length=10, blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perdidos'


class Pista(models.Model):
    idpista = models.AutoField(primary_key=True)
    idusuario = models.CharField(max_length=300, blank=True, null=True)
    idperdido = models.CharField(max_length=300, blank=True, null=True)
    asunto = models.CharField(max_length=500, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pista'


class Usuarios(models.Model):
    nombre = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.CharField(max_length=60, blank=True, null=True)
    clave = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
