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

@csrf_exempt
def list(request):
    data = {'categories':[]}
    categories = Categoria.objects.all().order_by('id').values()
    missing = Perdidos.objects.all().order_by('categoria').values()
    print('%d' % len(missing))
    missing_index = 0
    for category in categories:
        if missing_index == len(missing) - 1:
            print("Entro al if")
            break
        else:
            missing_category = {'name': category['nombre'], 'missing': []}
            while missing[missing_index]['categoria_id'] == category['id']:
                missing_category['missing'].append(missing[missing_index])
                missing_index+=1
                print('%d' % missing_index)
        data['categories'].append(missing_category)
    json_categoriasxperdidos= json.dumps(data)
    return HttpResponse(json_categoriasxperdidos, content_type= 'application/json')

@csrf_exempt
def clue(request):
    idUsuario = request.POST.get("idUser")
    idPerdido = request.POST.get("idLostPerson")
    asunto = request.POST.get("subject")
    descripcion = request.POST.get("description")
    data= {'result':False}
    if descripcion != "" and  asunto != "" and len(descripcion) <= 400 and len(asunto) <= 30:
        p= Pista(idusuario=idUsuario, idperdido= idPerdido, asunto= asunto, descripcion=descripcion)
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
