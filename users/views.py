from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

def login(request):

    data= {'resultado':True}
    	conn_string = "host='127.0.0.1' dbname='miapp_db' user='miapp' password='miapp'"
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()

	# execute our Query
	cursor.execute("SELECT * FROM Usuario")

	# retrieve the records from the database
	records = cursor.fetchall()

	# print out the records using pretty print
	# note that the NAMES of the columns are not shown, instead just indexes.
	# for most people this isn't very useful so we'll show you how to return
	# columns as a dictionary (hash) in the next example.
	pprint.pprint(records)
    json_data= json.dumps(data)
    print(json_data)
    return HttpResponse(json_data, content_type= 'application/json')

def register(request):

    data= {'resultado':False}
    json_data= json.dumps(data)
    return HttpResponse(json_data, content_type= 'application/json')
