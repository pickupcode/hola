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
<<<<<<< HEAD
    
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

=======




    nombrein= request.GET["name"]
    usuarioin= request.GET["username"]
    passwordin= request.GET["password"]

    #user_exists = user_exists(usuarioin)

    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    conn.autocommit = True
    #data= {'resultado':False}
    #if user_exists == False:
        #cursor= conn.cursor()
        #valores = (nombrein, usuarioin, passwordin)
        #query = 'INSERT INTO usuarios (nombre, usuario, clave) VALUES (%s,%s,%s)' % valores
        #cursor.execute(query)
        #conn.commit()
        #data= {'resultado': True}

    #json_data= json.dumps(data)
    #return HttpResponse(json_data, content_type= 'application/json')






    print('aqui esta la conexion')
    print(conn)
    cursor= conn.cursor()
    #query pinta usuario y clave
    cursor.execute('SELECT usuario, clave FROM usuarios')

    usuarios = cursor.fetchall()
    i= 0
    k= 0
    j= 0
    #
    for row in usuarios:

        print (row)

        print("usuario ubicado")
        print(usuarios[1][0])
        #clave ubicada
        #print("clave del usuario ubicado")
    #   #print(usuarios[1][1])
    #
    #     #convertir a json el usuario y clave no
    #     #json_usuario= json.dumps(usuarios[1])
    #     #print("el json")
    #     #print(json_usuario)
    #     #logica
        if usuarioin not in usuarios[i][0]:

             print(len(usuarios))
             total= len(usuarios)
             print("usuario revisado")
             print(usuarios[i][0])
             print("clave")
             print(usuarios[i][1])
             print("contador")
             j= j+1
             print(j)


             if j==total:


                 print("insertar el usuario")
                 cursor2= conn.cursor()
                 data=(nombrein,usuarioin,passwordin)
                 print(data)
                 cursor2.execute("""INSERT INTO usuarios (nombre, usuario, clave) VALUES (%s,%s,%s)""",data)
                 #p= Usuario(nombre= nombrein, usuario= usuarioin, clave= passwordin)
                 #p.save()
                 data= {'resultado':True}
                 json_data= json.dumps(data)
                 return HttpResponse(json_data, content_type= 'application/json')

                 print("usuario creado con exito")
        else:

             print("el usuario ya existe")
             data= {'resultado':False}
             json_data= json.dumps(data)
             return HttpResponse(json_data, content_type= 'application/json')

        i= i+1
>>>>>>> 3e2a25ea1c25b89540a1552943250aa0836af1e6
def listar(request):
    print("el usuario ya existe")
    data= {'categorias':[]}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')



#
