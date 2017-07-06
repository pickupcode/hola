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
# Create your views here12.

# MARK: - Check Methods
def incorrect_request_method():
    return HttpResponse('<h1>Ayy Lmao! This method is not allowed my dude</h1>', status = 405, content_type = 'text/html')

def check_parameters_data(*params):
    for param in params:
        if param is None:
            return HttpResponse('<h1>Ayy Lmao! You are missing some data my dude</h1>', status = 400, content_type = 'text/html')
    return None

def incorrect_content_type():
    return HttpResponse('<h1>Ayy Lmao! Not a JSON my dude</h1>', status = 415, content_type = 'text/html')

# MARK: - BusinessLogic Methods
@csrf_exempt
def login(request):
    # Check method
    if request.method != "POST":
        return incorrect_request_method()
    # Check content type
    if request.content_type != "application/json":
        return incorrect_content_type()

    data = json.loads(request.body)
    username = data.get('username', None)
    password = data.get('password', None)
    # Check parameters
    is_missing_parameters = check_parameters_data(username, password)
    if is_missing_parameters is not None:
        return is_missing_parameters

    users = Usuarios.objects.filter(usuario=username, clave=password).values()
    if len(users) != 1:
        data = {'username' : ""}
    else:
        user = users[0]
        data = user
        data.pop('clave', None)
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def user_exists(usuario):
    users = Usuarios.objects.filter(usuario=usuario)
    return True if len(users) == 1 else False

@csrf_exempt
def register(request):
    # Check method
    if request.method != "POST":
        return incorrect_request_method()
    # Check content type
    if request.content_type != "application/json":
        return incorrect_content_type()

    data = json.loads(request.body)
    # Check parameters
    is_missing_parameters = check_parameters_data(data.get('username', None),
                                                data.get('password', None),
                                                data.get('name', None))
    if is_missing_parameters is not None:
        return is_missing_parameters

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
        data = {'result': False}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def list(request):
    data = {'categories':[]}
    categories = Categoria.objects.all().order_by('id').values()
    missing = Perdidos.objects.all().order_by('categoria').values()
    missing_index = 0
    for category in categories:
        missing_category = {'name': category['nombre'], 'missing': []}
        while missing_index < len(missing) and missing[missing_index]['categoria_id'] == category['id']:
            missing_person = missing[missing_index]
            missing_person.pop('id', None)
            missing_person.pop('categoria_id', None)
            missing_category['missing'].append(missing_person)
            missing_index+=1
        data['categories'].append(missing_category)
        if not missing_index < len(missing):
            break
    json_categoriasxperdidos= json.dumps(data)
    return HttpResponse(json_categoriasxperdidos, content_type= 'application/json')

@csrf_exempt
def clue(request):
    # Check method
    if request.method != "POST":
        return incorrect_request_method()
    # Check content type
    if request.content_type != "application/json":
        return incorrect_content_type()

    data = json.loads(request.body)
    username = data.get('idUser', None)
    dni_missing = data.get('idLostPerson', None)
    subject = data.get('subject', None)
    clue = data.get('description', None)
    # Check parameters
    is_missing_parameters = check_parameters_data(username, dni_missing, subject, clue)
    if is_missing_parameters is not None:
        return is_missing_parameters

    data= {'result': False}
    if clue != "" and  subject != "" and len(clue) <= 400 and len(subject) <= 30:
        p = Pista(idusuario = username, idperdido = dni_missing, asunto = subject, descripcion = clue)
        p.save()
        data= {'result': True}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def report(request):
    # Check method
    if request.method != "POST":
        return incorrect_request_method()
    # Check content type
    if request.content_type != "application/json":
        return incorrect_content_type()

    data = json.loads(request.body)
    username = data.get('idUser', None)
    report = data.get('report', None)
    # Check parameters
    is_missing_parameters = check_parameters_data(username, report)
    if is_missing_parameters is not None:
        return is_missing_parameters

    dni_missing = data.get("idLostPerson", None)
    name_missing = data.get("name", None)
    data= {'result':False}
    if report != ""  and len(report) <= 600:
        p = Denuncia(idusuario = username, idperdido = dni_missing, detalle = report, nombre = name_missing)
        p.save()
        data= {'result': True}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def test(request):
    data = {'test' : "Ay Lmao ay lmao"}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')
