#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import blast as bs
import muscle as mc
import dominios as dm
import argparse

#Función de ayuda:
def help():
	"""
	
	h = (
	USAGE: python3 main.py query subject cov identity
	-query: ruta del archivo en formato fasta que contiene una o varias
	secuencias de proteínas. Si se quieren analizar varias secuencias
	estas deben encontrarse en el mismo archivo.
	-subject: ruta a la carpeta llamada genbank en la cual hay uno o varios
	genbanks
	-cov: argumento opcional. Número entre 0 y 100 que indica el porcentaje
	mínimo de cobertura para filtar los resultados al hacer blastp
	-identity: argumento opcional. Número entre 0 y 100 que indica el
	porcentaje de identidad mínimo para filtar los resultados al hacer blastp
	)
	"""
	print(h)
	sys.exist

arguments = sys.argv
for argument in arguments:
	if argument == "-h":
		help()
		sys.exit()

#Definición argumentos obligatorios
query = sys.argv[1]
subject = sys.argv[2]

#Definición argumentos opcionales
if len(sys.argv) == 3:
	cov = 50
	identity = 25
elif len(sys.argv) == 5:
	cov = sys.argv[3]
	identity = sys.argv[4]
else:
	print("Error: number of arguments introduced is not valid")
	help()
	sys.exist()


#Ejecución del blast.py:
bs.multifasta(subject)
bs.database()
dicti = bs.dictionary(query)
output = bs.blastp(query)
bs.finalblast(cov, identity, dicti)

#Ejecución de muscle.py:
mc.muscle()

#Ejecución de dominios.py:
a = dm.parsear()
dictionary = dm.dicti()
dm.search(dictionary)