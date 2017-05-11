from django.shortcuts import render
from django.http import HttpResponse
from users.models import Usuario

import json
import psycopg2
import sys
import pprint
# Create your views here.

def login(request):
    #print("usuario geteado")

    #usuarioget=request.GET["username"]
    #print(usuarioget)
    #print("clave geteado")
    #claveget=request.GET["password"]

    #data= {'resultado':True}

    usuariobd= request.GET["username"]
    clavebd = request.GET["password"]
    # data2={'User':{'usuario': usuariobd, 'clave': clavebd}}
    # # json_data2= json.dumps(data2)
    # print("nuevo json")
    # print(json_data2)


    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    # print('aqui esta la conexion')
    # print(conn)
    cursor= conn.cursor()
    #query pinta usuario y clave
    query = 'SELECT usuario, clave FROM usuarios WHERE usuario = %s' % usuariobd
    cursor.execute(query)

    # Result Set
    rs = cursor.fetchall()
    data= {'usuario': "", 'clave': ""}
    if rs.rowcount > 0:
        #rs.1 es la clave
        if clavebd == rs[1]:
            #Usuario y Password Correcto
            data = {'usuario': usuariobd, 'clave': clavebd}

    json_data= json.dumps(data)
    print(json_data)
    return HttpResponse(json_data, content_type= 'application/json')

    # usuarios = cursor.fetchall()
    # #print(usuarios)
    # i=0
    # for row in usuarios:
    #     print (row)
    #     #usuario ubicado
    #     #print("usuario ubicado")
    #     print(usuarios[1][0])
    #     #clave ubicada
    #     #print("clave del usuario ubicado")
    #     print(usuarios[1][1])
    #
    #     #convertir a json el usuario y clave no
    #     #json_usuario= json.dumps(usuarios[1])
    #     #print("el json")
    #     #print(json_usuario)
    #     #logica
    #     if usuariobd in usuarios[i][0] and clavebd in usuarios[i][1]:
    #         print("clave")
    #         print(usuarios[i][1])
    #         print("el usuario existe")
    #         #data= {'resultado':True}
    #         data={'usuario': usuariobd, 'clave': clavebd}
    #         json_data= json.dumps(data)
    #         print(json_data)
    #         return HttpResponse(json_data, content_type= 'application/json')
    #     elif usuariobd in usuarios[i][0] and clavebd not in usuarios[i][1]:
    #         print("La contrasena no es correcta")
    #         data= {'usuario': "", 'clave': ""}
    #         json_data= json.dumps(data)
    #         print(json_data)
    #         return HttpResponse(json_data, content_type= 'application/json')
    #     elif usuariobd not in usuarios[i][0] and clavebd in usuarios[i][1]:
    #         print("usuario no esta registrado")
    #         data= {'usuario': "", 'clave': ""}
    #         json_data= json.dumps(data)
    #         print(json_data)
    #         return HttpResponse(json_data, content_type= 'application/json')
    #     #elif usuariobd not in usuarios[i][0] and clavebd not in usuarios[i][1]:
    #         #print("La contrasena no es correcta")
    #         #data= {'resultado':False}
    #         #json_data= json.dumps(data)
    #         #print(json_data)
    #         #return HttpResponse(json_data, content_type= 'application/json')
    #     else:
    #         print("informacion incorrecta")
    #         data= {'usuario': "", 'clave': ""}
    #         json_data= json.dumps(data)
    #         print(json_data)
    #         return HttpResponse(json_data, content_type= 'application/json')
    #     #puntero
    #     i= i+1
    #     print (i)



    #json_data= json.dumps(data)
    #print(json_data)
    #return HttpResponse(json_data, content_type= 'application/json')

def user_exists(usuario):
    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    cursor= conn.cursor()
    query = 'SELECT usuario, clave FROM usuarios WHERE usuario = %s' % usuario
    cursor.execute(query)

    # Result Set
    rs = cursor.fetchall()
    return False if rs.rowcount == 0 else False

def register(request):



    nombrein= request.GET["name"]
    usuarioin= request.GET["username"]
    passwordin= request.GET["password"]

    user_exists = user_exists(usuarioin)

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
        usuario ubicado
        print("usuario ubicado")
        print(usuarios[1][0])
        #clave ubicada
        #print("clave del usuario ubicado")
    #     #print(usuarios[1][1])
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
def listar(request):
    print("el usuario ya existe")
    data= {'categorias':[]}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')
