from django.shortcuts import render
from django.http import HttpResponse
from users.models import Usuario

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
    query = "SELECT c.id, c.nombre, p.dni, p.firstname, p.edad, p.descripcion, p.lastname, p.categoria FROM \"Categoria\" as c join \"perdidos\" as p on c.id = p.categoria order by c.id"
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

        perdido = {'nombre' : result[3], 'apellido' : result[6], 'dni' : result[2], 'age' : result[4], 'description' : result[5]}
        data['categorias'][previous_category_index]['perdidos'].append(perdido)

    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

def clue(request):
    print ("entro a clues dasdad")

    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    data= {'resultado':False}
    cursor= conn.cursor()

    query = "INSERT INTO pista (idusuario, idperdido, asunto, descripcion) VALUES ('%s','%s','%s','%s')" % (1,2,sadsad,sadad)


    if descripcion != descripcion.empty or  asunto != asunto.empty:
        cursor.execute(query)
        conn.commit()
        data= {'resultado': True}
        json_data= json.dumps(data)
        return HttpResponse(json_data, content_type= 'application/json')

    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')


def test(request):
    data = {'test' : "Ay Lmao"}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')

#
