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
    return True if (len(users) != 1) else False

@csrf_exempt
def register(request):
    data = json.loads(request.body)
    print(data)
    users = serializers.deserialize('json', data)
    print(users)
    data = {'result':False}
    # if not user_exists(user.usuario):
    #     print('user does not exist')
    #     user.save()
    #     data= {'result': True}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')


    # nombrein= request.POST.get("name")
    # usuarioin= request.POST.get("username")
    # passwordin= request.POST.get("password")
    # dniin= request.POST.get("dni",None)
    # emailin= request.POST.get("email",None)
    # edadin = request.POST.get("age",None)
    # usuario_jango= Usuarios.objects.filter(usuario=usuarioin)
    # user_does_exist = user_exists(usuarioin)
    # data= {'result':False}
    # if user_does_exist == False:
    #     p = Usuarios(nombre=nombrein, usuario=usuarioin, clave=passwordin, dni=dniin, email=emailin, edad= edadin)
    #     p.save()
    #     data= {'result': True}
    # json_data= json.dumps(data)
    # return HttpResponse(json_data, content_type= 'application/json')

@csrf_exempt
def list(request):
    lista_categoria= Categoria.objects.all().order_by('id')
    categoria_json= serializers.serialize('json',lista_categoria)
    data = {'categories':[]}
    categoria = {'name' : "", 'missing' : []}
    i=0
    for categ in lista_categoria.iterator():
        pk_categoria= categ.id
        lista_perdido= Perdidos.objects.filter(categoria=pk_categoria).order_by('categoria')
        perdido_json=serializers.serialize('json',lista_perdido)
        categori= {'name': categ.nombre, 'missing': []}
        data['categorias'].append(categori)
        i= i+1
        for perdido in lista_perdido.iterator():
            perdid= {'nombre': perdido.firstname, 'apellido': perdido.lastname, 'dni': perdido.dni, 'age': perdido.edad, 'description': perdido.descripcion, 'imagen': perdido.imagen}
            data['categorias'][i-1]['perdidos'].append(perdid)
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
