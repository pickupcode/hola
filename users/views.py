from django.shortcuts import render
from django.http import HttpResponse
import json
import psycopg2
import sys
import pprint
# Create your views here.

def login(request):

    data= {'resultado':True}
    #conn_string = "dbname='miapp_db' user='miapp' password='miapp'"
    #print ("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect("host=ec2-174-129-227-116.compute-1.amazonaws.com dbname=ddgrh85co1hhsd user=txmdzfeapxbwss password=27fd84a2984d45a8416526ce6c1dae1985e8a2de97970fcf21739e79106e6299")
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
