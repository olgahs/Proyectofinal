#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
from Bio.ExPASy import Prosite, Prodoc
import os

def parsear():
	"""
	Parsear a file.dat with Prosite. Extraction of the name, accession,
	pattern and description.
	"""
	inpfile = 'prosite.dat'
	path1 = "results/prosite"
	try:
		os.stat(path1)
	except:
		os.mkdir(path1)
	
	out = open(path1 + "database", "w")
	handle = open(inpfile, "r")
	records = Prosite.parse(handle)
	for record in records:
		out.write(record.name + "\t")
		out.write(record.accession + "\t")
		out.write(record.description + "\t")
		out.write(record.pattern + "\n")
	handle.close()
	out.close()

def dicti():
	"""
	Make a dictionary with accession (key) and the domain value of each
	accession.
	"""
	dictio = dict()
	inp = open('results/prosite/database', "r")

	for row in inp:
		colums = row.split("\t")
		name = colums[0]
		accession = colums[1]
		pattern = colums[2].strip()
		pattern = pattern.replace("(", "{")
		pattern = pattern.replace(")", "}")
		pattern = pattern.replace("x", ".")
		pattern = pattern.replace("-", "")
		pattern = pattern.split()
		description = colums[3]

		if pattern == "":
			pass
		else:
			dictio[accession] = [pattern, name, description]
	inp.close()
	return dictio

def search(dictionary):
	"""
	Parsear fasta files of Blastp with proteins sequences about what we
	want the domains
	"""
	pat = "results/"
	for inp in os.listdir(pat):
		file1 = open(pat + inp,"r")
		file2 = "results/prosite" + inp[:-3] + "_dominios.txt"
		file3 = open(file2, "w")

		for rows in file1:
			if rows.startswith(">"):
				id = rows
				id = id[1:]
				file3.write(id + "\n")
			elif rows.startswith("\n") == False:
				sequences = rows.strip()
				c = 0
				for key in dictionary:
					f = re.compile(dictionary[key][0])
					g = f.search(sequences)
					if g == "":
						pass
					else:
						c += 1
						result = g.group()
						file3.write("Domain number" + " " + str(c) + " " + "Domain \n" + "Domain name" + dictionary[key][1] + "\n" + "Accession" + key + "\n" + "Pattern" + str(result) + "\n" + "Description" + dictionary[key][2] + "\n")
			else:
				pass
	file1.close()
	file3.close()
