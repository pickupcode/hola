from django.shortcuts import render
from django.http import HttpResponse

import json
import psycopg2
import sys
import pprint
# Create your views here.

def login(request):

    data= {'resultado':True}

    usuariobd= "edvs"
    clavebd = "abc"


    conn = psycopg2.connect("dbname='ddgrh85co1hhsd' user='txmdzfeapxbwss' password='27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299' host='ec2-174-129-227-116.compute-1.amazonaws.com' port='5432'")
    print('aqui esta la conexion')
    print(conn)
    cursor= conn.cursor()
    #query pinta usuario y clave
    cursor.execute('SELECT usuario, clave FROM "Usuario"')


    usuarios = cursor.fetchall()
    #print(usuarios)
    i=0
    for row in usuarios:
        #print (row)
        #usuario ubicado
        #print("usuario ubicado")
        #print(usuarios[1][0])
        #clave ubicada
        #print("clave del usuario ubicado")
        #print(usuarios[1][1])

        #convertir a json el usuario y clave no
        #json_usuario= json.dumps(usuarios[1])
        #print("el json")
        #print(json_usuario)
        #logica
        if usuariobd in usuarios[i][0] and clavebd in usuarios[i][1]:
            print("clave")
            print(usuarios[i][1])
            print("el usuario existe")
            data= {'resultado':True}
            json_data= json.dumps(data)
            print(json_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif usuariobd in usuarios[i][0] and clavebd not in usuarios[i][1]:
            print("La contrasena no es correcta")
            data= {'resultado':False}
            json_data= json.dumps(data)
            print(json_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif usuariobd not in usuarios[i][0] and clavebd in usuarios[i][1]:
            print("La contrasena no es correcta")
            data= {'resultado':False}
            json_data= json.dumps(data)
            print(json_data)
            return HttpResponse(json_data, content_type= 'application/json')
        elif usuariobd not in usuarios[i][0] and clavebd not in usuarios[i][1]:
            print("La contrasena no es correcta")
            data= {'resultado':False}
            json_data= json.dumps(data)
            print(json_data)
            return HttpResponse(json_data, content_type= 'application/json')
        #else:
            #print("informacion incorrecta")
            #data= {'resultado':False}
            #json_data= json.dumps(data)
            #print(json_data)
            #return HttpResponse(json_data, content_type= 'application/json')
        #puntero
        i= i+1
        print (i)



    #json_data= json.dumps(data)
    #print(json_data)
    #return HttpResponse(json_data, content_type= 'application/json')

def register(request):

    data= {'resultado':False}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')
