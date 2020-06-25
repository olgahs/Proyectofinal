#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import call
import sys
import os
#Alineamiento de secuencias y creación de árbol filogenético con MUSCLE
def muscle():
	"""
	Muscle aligment and creating filogenetic tree
	"""
	#Creamos un bucle por si hay más de un archivo blastfinal
	path1 = "results/muscle"
	try:
		os.stat(path1)
	except:
		os.mkdir(path1)
	path = "results/"
	for c in os.listdir(path):
		inp = path + c
		out = path1 + "/" + c[:-3] + ".aligment"
	#Alineamiento:
		cmd3 = ['muscle', '-in', inp, '-out', out]
		try:
			call(cmd3)
		except:
			print("muscle aligment failed")
			sys.exit()
	#Creación árbol:
	out_arbol = path1 + "/" + c[:-3] + ".tree.nw"
	cmd4 = ['muscle', '-maketree', '-in', out, '-out', out_arbol, '-cluster', 'neighborjoining']
	try:
		call(cmd4)
	except:
		print("maketree failed")
		sys.exit()