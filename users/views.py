from django.shortcuts import render
from django.http import HttpResponse
from users.models import Usuarios
from users.models import Pista
from users.models import Perdidos
from users.models import Categoria
from django.core import serializers

import json
import psycopg2
import sys
import pprint
# Create your views here.

def login(request):

    usuariobd= request.GET["username"]
    clavebd = request.GET["password"]

    #conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")

    #cursor= conn.cursor()
    #query pinta usuario y clave
    #query = "SELECT nombre, usuario, clave FROM usuarios WHERE usuario = '%s'" % usuariobd
    #cursor.execute(query)
    usuario_jango= Usuarios.objects.filter(usuario=usuariobd)
    print("imprimiste un usuario filtrado")
    for i in usuario_jango.iterator():
        print(i.usuario)
        print(i.nombre)
        print(i.clave)
    # Result Set
    #rs = cursor.fetchall()
        data= {'nombre' : "", 'usuario' : "", 'clave' : ""}
        if usuario_jango.count() > 0:
        #rs.1 es la clave
            if clavebd == i.clave:
            #Usuario y Password Correcto
                nombre = i.nombre
                usuario = i.usuario
                clave = i.clave
                data = {'nombre': nombre,'usuario': usuario, 'clave': clave}

                json_data= json.dumps(data)
                print(json_data)
                return HttpResponse(json_data, content_type= 'application/json')

def user_exists(usuario):
    #conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    #cursor= conn.cursor()
    #query = "SELECT usuario FROM usuarios WHERE usuario = '%s'"  % usuario
    #cursor.execute(query)
    usuario_jango= Usuarios.objects.filter(usuario=usuario)
    # Result Set
    #rs = cursor.fetchall()
    user_does_exist = usuario_jango.count() == 1
    return True if user_does_exist else False


def register(request):

    nombrein= request.GET["name"]
    usuarioin= request.GET["username"]
    passwordin= request.GET["password"]
    usuario_jango= Usuarios.objects.filter(usuario=usuarioin)
    #for usuario in usuario_jango:
        #print("existe?")
        #print(usuario_jango.count())
    user_does_exist = user_exists(usuarioin)

    #conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    data= {'resultado':False}
    if user_does_exist == False:
        #cursor= conn.cursor()
        #valores = (nombrein, usuarioin, passwordin)
        #query = "INSERT INTO usuarios (nombre, usuario, clave) VALUES ('%s','%s','%s')" % valores
        #cursor.execute(query)
        #conn.commit()
        p= Usuarios(nombre=nombrein, usuario=usuarioin, clave=passwordin)
        p.save()
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
        print(current_result_category_id)
        previous_result_category_id = rs[rs.index(result)-1][0] if current_category_index >= 0 else ""
        print(previous_result_category_id)
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
    #conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")

    if descripcion != "" and  asunto != "" and len(descripcion) <= 400 and len(asunto) <= 30:
        #valores = (idUsuario, idPerdido, asunto,descripcion)
        #cursor= conn.cursor()
        #query = "INSERT INTO pista (idusuario, idperdido, asunto, descripcion) VALUES ('%s','%s','%s','%s')" % valores
        #cursor.execute(query)
        #conn.commit()
        p= Pista(idusuario=idUsuario, idperdido= idPerdido, asunto= asunto, descripcion=descripcion)
        p.save()
        data= {'resultado': True}
        json_data= json.dumps(data)
        return HttpResponse(json_data, content_type= 'application/json')

    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')


def test(request):
    lista_usuarios= Usuarios.objects.all()
    lista_pistas= Pista.objects.all()

    #for pista in lista_pistas:
        #print(pista.idpista)
        #print("--------")
    #ya se pueden hacer querys con django!!!!!!!!!!!!!!
    json_estudiantes= serializers.serialize('json',lista_usuarios)
    #print(json_estudiantes)
    #p= Usuarios(nombre="prueba32", usuario="p32", clave="abc")
    #p.save()
    #for usuario in lista_usuarios:
        #print(usuario.usuario)
    #armando el json listar
    #lista_perdido= Perdidos.objects.select_related()
    lista_categoria= Categoria.objects.all().order_by('id')
    categoria_json= serializers.serialize('json',lista_categoria)
    #print(categoria_json)
    #print("otro json")
    #perdido_json= serializers.serialize('json',lista_perdido)
    #print(perdido_json)
    i=0
    j=0
    data = {'categorias':[]}
    categoria = {'nombre' : "", 'perdidos' : []}
    #for perdido in lista_perdido:
        #print(perdido.firstname)
    print("ids categorias")
    for categ in lista_categoria.iterator():

        pk_categoria= categ.id
        #print(pk_categoria)
        lista_perdido= Perdidos.objects.filter(categoria=pk_categoria).order_by('categoria')
        perdido_json=serializers.serialize('json',lista_perdido)
        #print(perdido_json)
        for perdido in lista_perdido.iterator():
            categoria= {'nombre': categ.nombre, 'perdidos': []}
            data['categorias'].append(categoria)
            perdido= {'nombre': perdido.firstname, 'apellido': perdido.lastname, 'dni': perdido.dni, 'age': perdido.edad, 'description': perdido.descripcion, 'imagen': perdido.imagen}
            #print(perdido)
            print(data['categorias'][0]['perdidos'])
            data['categorias'][i]['perdidos'].append(perdido)
            i= i+1
            j= j+1
    print(data)
    json_categoriasxperdidos= json.dumps(data)



    #data = {'test' : "Ay Lmao ay lmao sdad2"}
    #json_data= json.dumps(data)
    return HttpResponse(json_categoriasxperdidos, content_type= 'application/json')

#
