#!/usr/bin/python
# -*- coding: UTF-8 -*-
#Rutina python/PostGIS para dividir lineas en segmentos y conservar los mismos atributos

import os, psycopg2
conn = psycopg2.connect(database="database_name_here", user="******", password="******", host="127.0.0.1", port="5432")


def dividolinea( idlinea ):
	"""Divide linea
    Pasarle como parámero el id de la linea y la dividirá en 10 tramos
    """
	idlin=idlinea
	print 'voy a dividir la ', idlin
	for i in range(0,10):
		inicio=i/10.0
		fin = (i/10.0)+0.1
		#Creo segmentos
		sql ="insert into redvial_contramos (id, geom, idsegmento) values (%d ,ST_Line_Substring((select geom from vial where id= %d ), %f,%f), %d%d);" % (idlin, idlin, inicio, fin, idlin, i)
		print sql
		#Añado atributos
		sql2= "update redvial_contramos set coste=(select coste from redvial where id=%d), id_tramo=(select id_tramo from redvial where id=%d), tipovia=(select tipovia from redvial where id=%d), nomvia=(select nomvia from redvial where id=%d), velocidad=(select velocidad from redvial where id=%d) where id=%d;" % (idlin, idlin, idlin, idlin, idlin, idlin)
		print sql2
		cur = conn.cursor()
		cur.execute(sql)
		conn.commit()
		cur = conn.cursor()
		cur.execute(sql2)
		conn.commit()
		
		print "Linea insertada con exito"


#conecto y pido las ids
cur = conn.cursor()
cur.execute("select id, st_length(geom) from vial where st_length(geom) > 5000")
rows = cur.fetchall()
listaCalles=[]
for row in rows:
	listaCalles.append(row[0])

for p in listaCalles:
	dividolinea(p)


conn.close()

#Todo:
#Preguntar a partir de qué tamaño quieres cortar
#Crear tabla nueva dinámicamente
	
