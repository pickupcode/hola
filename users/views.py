from django.shortcuts import render
from django.http import HttpResponse
from users.models import Usuarios
from users.models import Pista
from users.models import Perdidos
from users.models import Categoria
from users.models import Denuncia
from django.core import serializers

import json
import psycopg2
import sys
import pprint
# Create your views here.

def login(request):
    usuariobd= request.GET["username"]
    clavebd = request.GET["password"]
    usuario_jango= Usuarios.objects.filter(usuario=usuariobd)
    user = usuario_jango.iterator():
        data= {'nombre' : "", 'usuario' : "", 'clave' : ""}
        if usuario_jango.count() > 0:
            if clavebd == i.clave:
            #Usuario y Password Correcto
                nombre = i.nombre
                usuario = i.usuario
                clave = i.clave
                data = {'nombre': nombre,'usuario': usuario, 'clave': clave}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def user_exists(usuario):
    usuario_jango= Usuarios.objects.filter(usuario=usuario)
    user_does_exist = usuario_jango.count() == 1
    return True if user_does_exist else False


def register(request):
    nombrein= request.GET["name"]
    usuarioin= request.GET["username"]
    passwordin= request.GET["password"]
    dniin= request.GET.get("dni",None)
    emailin= request.GET.get("email",None)
    edadin = request.GET.get("edad",None)
    usuario_jango= Usuarios.objects.filter(usuario=usuarioin)
    user_does_exist = user_exists(usuarioin)
    data= {'resultado':False}
    if user_does_exist == False:
        p = Usuarios(nombre=nombrein, usuario=usuarioin, clave=passwordin, dni=dniin, email=emailin, edad= edadin)
        p.save()
        data= {'resultado': True}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def listar(request):
    lista_categoria= Categoria.objects.all().order_by('id')
    categoria_json= serializers.serialize('json',lista_categoria)
    data = {'categorias':[]}
    categoria = {'nombre' : "", 'perdidos' : []}
    for categ in lista_categoria.iterator():
        pk_categoria= categ.id
        lista_perdido= Perdidos.objects.filter(categoria=pk_categoria).order_by('categoria')
        perdido_json=serializers.serialize('json',lista_perdido)
        categori= {'nombre': categ.nombre, 'perdidos': []}
        data['categorias'].append(categori)
        i= i+1
        for perdido in lista_perdido.iterator():
            perdid= {'nombre': perdido.firstname, 'apellido': perdido.lastname, 'dni': perdido.dni, 'age': perdido.edad, 'description': perdido.descripcion, 'imagen': perdido.imagen}
            data['categorias'][i-1]['perdidos'].append(perdid)
    json_categoriasxperdidos= json.dumps(data)
    return HttpResponse(json_categoriasxperdidos, content_type= 'application/json')

def clue(request):
    idUsuario = request.GET["idUsuario"]
    idPerdido = request.GET["idPerdido"]
    asunto = request.GET["asunto"]
    descripcion = request.GET["descripcion"]
    data= {'resultado':False}
    if descripcion != "" and  asunto != "" and len(descripcion) <= 400 and len(asunto) <= 30:
        p= Pista(idusuario=idUsuario, idperdido= idPerdido, asunto= asunto, descripcion=descripcion)
        p.save()
        data= {'resultado': True}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def report(request):
    idusuario = request.GET["idUsuario"]
    idperdido = request.GET["idPerdido"]
    dni = request.GET["DNI"]
    nombre = request.GET["Nombre"]
    detalle = request.GET["Detalle"]
    data= {'resultado':False}
    if detalle != "" and  dni != "" and len(detalle) <= 600 and len(dni) <= 10:
        p= Denuncia(idusuario=idusuario, idperdido= idperdido, dni= dni, detalle=detalle,nombre=nombre)
        p.save()
        data= {'resultado': True}
        json_data= json.dumps(data)
        return HttpResponse(json_data, content_type= 'application/json')
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def test(request):
    data = {'test' : "Ay Lmao ay lmao sdad2"}
    json_data= json.dumps(data)
    return HttpResponse(json_categoriasxperdidos, content_type= 'application/json')
