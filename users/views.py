from django.shortcuts import render
from django.http import HttpResponse
from users.models import Usuarios
from django.core import serializers

import json
import psycopg2
import sys
import pprint
# Create your views here.

def login(request):

    usuariobd= request.GET["username"]
    clavebd = request.GET["password"]

    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")

    cursor= conn.cursor()
    #query pinta usuario y clave
    query = "SELECT nombre, usuario, clave FROM usuarios WHERE usuario = '%s'" % usuariobd
    cursor.execute(query)
    usuario_jango= Usuarios.objects.filter(usuario="edvs")
    print("imprimiste un usuario filtrado")
    print(usuario_jango)
    # Result Set
    rs = cursor.fetchall()
    data= {'nombre' : "", 'usuario' : "", 'clave' : ""}
    if len(rs) > 0:
        #rs.1 es la clave
        if clavebd == rs[0][2]:
            #Usuario y Password Correcto
            nombre = rs[0][0]
            usuario = rs[0][1]
            clave = rs[0][2]
            data = {'nombre': nombre,'usuario': usuario, 'clave': clave}

    json_data= json.dumps(data)
    print(json_data)
    return HttpResponse(json_data, content_type= 'application/json')

def user_exists(usuario):
    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    cursor= conn.cursor()
    query = "SELECT usuario FROM usuarios WHERE usuario = '%s'"  % usuario
    cursor.execute(query)

    # Result Set
    rs = cursor.fetchall()
    user_does_exist = len(rs) == 1
    return True if user_does_exist else False

def register(request):

    nombrein= request.GET["name"]
    usuarioin= request.GET["username"]
    passwordin= request.GET["password"]

    user_does_exist = user_exists(usuarioin)

    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    data= {'resultado':False}
    if user_does_exist == False:
        cursor= conn.cursor()
        valores = (nombrein, usuarioin, passwordin)
        query = "INSERT INTO usuarios (nombre, usuario, clave) VALUES ('%s','%s','%s')" % valores
        cursor.execute(query)
        conn.commit()
        data= {'resultado': True}
        json_data= json.dumps(data)
        return HttpResponse(json_data, content_type= 'application/json')

    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def listar(request):
    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    cursor= conn.cursor()
    #query pinta usuario y clave
    query = "SELECT c.id, c.nombre, p.dni, p.firstname, p.edad, p.descripcion, p.lastname, p.categoria, p.imagen FROM \"Categoria\" as c join \"perdidos\" as p on c.id = p.categoria order by c.id"
    cursor.execute(query)
    # Result Set
    rs = cursor.fetchall()
    data = {'categorias':[]}
    categoria = {'nombre' : "", 'perdidos' : []}
    current_category_index = 0
    previous_category_index = -1
    for result in rs:
        current_result_category_id = result[0]
        previous_result_category_id = rs[rs.index(result)-1][0] if current_category_index >= 0 else ""
        if current_result_category_id != previous_result_category_id:
            previous_category_index = current_category_index
            current_category_index += 1
            categoria = {'nombre' : result[1], 'perdidos' : []}
            data['categorias'].append(categoria)
        imagenRaw = str(result[8])
        perdido = {'nombre' : result[3], 'apellido' : result[6], 'dni' : result[2], 'age' : result[4], 'description' : result[5], 'imagen' : imagenRaw}
        data['categorias'][previous_category_index]['perdidos'].append(perdido)

    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def clue(request):
    idUsuario = request.GET["idUsuario"]
    idPerdido = request.GET["idPerdido"]
    asunto = request.GET["asunto"]
    descripcion = request.GET["descripcion"]
    data= {'resultado':False}
    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")

    if descripcion != "" and  asunto != "" and len(descripcion) <= 400 and len(asunto) <= 30:
        valores = (idUsuario, idPerdido, asunto,descripcion)
        cursor= conn.cursor()
        query = "INSERT INTO pista (idusuario, idperdido, asunto, descripcion) VALUES ('%s','%s','%s','%s')" % valores
        cursor.execute(query)
        conn.commit()
        data= {'resultado': True}
        json_data= json.dumps(data)
        return HttpResponse(json_data, content_type= 'application/json')

    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')


def test(request):
    lista_usuarios= Usuarios.objects.all()
    #ya se pueden hacer querys con django!!!!!!!!!!!!!!
    json_estudiantes= serializers.serialize('json',lista_usuarios)
    print(json_estudiantes)
    for usuario in lista_usuarios:
        print(usuario.usuario)
    data = {'test' : "Ay Lmao ay lmao sdad2"}
    json_data= json.dumps(data)
    return HttpResponse(json_estudiantes, content_type= 'application/json')

#
