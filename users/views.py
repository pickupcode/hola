from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from users.models import Usuarios
from users.models import Pista
from users.models import Perdidos
from users.models import Categoria
from users.models import Denuncia


import json
import psycopg2
import sys
import pprint
# Create your views here.
@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    users = Usuarios.objects.filter(usuario=username, clave=password).values()
    if len(users) != 1:
        data = {'username' : ""}
    else:
        user = users[0]
        data = user
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def user_exists(usuario):
    users = Usuarios.objects.filter(usuario=usuario)
    return True if len(users) == 1 else False

@csrf_exempt
def register(request):
    data = json.loads(request.body)
    if not user_exists(data['username']):
        user = Usuarios(nombre = data['name'],
                        usuario = data['username'],
                        clave = data['password'],
                        dni = data.get('dni', None),
                        email = data.get('email', None),
                        edad = data.get('age', None))
        user.save()
        data= {'result': True}
    else:
        data = {'result':False}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def category_matches(cat_a, cat_b):
    return True if cat_a == cat_b else False

def in_range(index, length):
    return True if missing_index < length else False

@csrf_exempt
def list(request):
    data = {'categories':[]}
    categories = Categoria.objects.all().order_by('id').values()
    missing = Perdidos.objects.all().order_by('categoria').values()
    missing_index = 0
    for category in categories:
        missing_category = {'name': category['nombre'], 'missing': []}
        while missing_index < len(missing) and missing[missing_index]['categoria_id'] == category['id']:
            missing_category['missing'].append(missing[missing_index])
            missing_index+=1
        data['categories'].append(missing_category)
        if not missing_index < len(missing):
            break
    json_categoriasxperdidos= json.dumps(data)
    return HttpResponse(json_categoriasxperdidos, content_type= 'application/json')

@csrf_exempt
def clue(request):
    data = json.loads(request.body)
    username = data['idUser']
    dni_missing = data['idLostPerson']
    subject = data['subject']
    clue = data['description']
    data= {'result':False}
    if clue != "" and  subject != "" and len(clue) <= 400 and len(subject) <= 30:
        p= Pista(idusuario = username, idperdido = dni_missing, asunto = subject, descripcion = clue)
        p.save()
        data= {'result': True}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def report(request):
    idusuario = request.POST.get("idUser")
    idperdido = request.POST.get("idLostPerson",None)
    nombre = request.POST.get("name",None)
    detalle = request.POST.get("report")
    data= {'result':False}
    if detalle != ""  and len(detalle) <= 600:
        p= Denuncia(idusuario=idusuario, idperdido= idperdido, detalle=detalle,nombre=nombre)
        p.save()
        data= {'result': True}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def test(request):
    data = {'test' : "Ay Lmao ay lmao"}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')
