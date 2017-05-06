from django.shortcuts import render
from django.http import HttpResponse
import json
import psycopg2
import sys
import pprint
# Create your views here.

def login(request):

    data= {'resultado':True}
    conn_string = "host='127.0.0.1' dbname='miapp_db' user='miapp' password='miapp'"
    print ("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM Usuario")
    usuarios = cursor.fetchall
    print(usuarios)
    json_data= json.dumps(data)
    print(json_data)
    return HttpResponse(json_data, content_type= 'application/json')

def register(request):

    data= {'resultado':False}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')
