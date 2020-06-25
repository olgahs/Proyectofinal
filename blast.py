#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from Bio import SeqIO
#from Bio.Blast.Applications import NcbiblastpCommandline
from subprocess import call, DEVNULL, STDOUT
import os
from re import sub

#Convertir genbank a un multifasta

def multifasta(subject):
	"""
	Conversion of all genebanks files stored in one folder
	that the user choose to an unic multifasta file
	"""
	#Se comprueba si el multifasta existe previamente. Si existe se borra
	
	if os.path.isfile("multifasta.fa") == True:
		os.remove("multifasta.fa")
	else:
		pass

	file = open("multifasta.fa","a")

	for genbanks in os.listdir(subject):
		if os.path.isfile(subject+genbanks) == True:
			with open(subject+genbanks,"r") as input_handle:
				for record in SeqIO.parse(input_handle,"genbank"):
					for feature in record.features:
						if feature.type == 'CDS':
							try:
								seqprot = feature.qualifiers['translation'][0]
							except:
								seqprot = "empty"
							if seqprot != "empty":
								seq = seqprot.upper()
								seq = sub('(.{60})(.)',r'\1\n\2',seq)
								file.write(">" + feature.qualifiers['locus_tag'][0] + "\n" + seq + "\n")
	file.close()


#Creación de base de datos en la carpeta DB comprobando previamente si existe

def database():
	"""
	Blast database cration
	"""
#Creación de carpeta para almacenar la base de datos
#comprobando antes si ya existe dicha carpeta
	path1 = "database/"
	try:
		os.stat(path1)
	except:
		os.mkdir(path1)

	multifasta = "multifasta.fa"
	db = "database/database"
	cmd = [ 'makeblastdb','-dbtype','prot','-parse_seqids','-in',multifasta,'-out',db ]
	try:
		call(cmd)
	except:
		print("BLAST database creation failed")
		sys.exit()
	return db


def dictionary(query):
	"""
	Create a dictionary with query names (keys) and sequences
	"""
	dic_tionary = dict()
	qseq = str()
	a = 0
	f = open(query,"r")
	for line in f:
		if line.startswith(">"):
			if a !=0:
				dic_tionary[qid] = qseq
				qseq = str()
			#strip nos permite eliminar los espacios
			qid = line.strip()
			qid = qid[1:]
			a = 1
		elif line.startswith("\n") == False:
			qseq = qseq + line.strip()
		else:
			continue
	dic_tionary[qid] = qseq
	f.close()
	return dic_tionary


#Ejecución blastP con el multifasta creado anteriormente
#La identidad y el coverage pueden ser introducidas por el usuario
#Si no, son definidas como 30 y 50 respectivamente

def blastp(query):
	"""
	BlastP implementation
	"""
	
	folder = "database/database"
	out = "output_blast"
	cmd2 = [ 'blastp','-query',query,'-db',folder,'-outfmt','6 qseqid sseqid qcovs pident evalue','-evalue','0.00001','-out',out ]
	
	try:
		call(cmd2)
	except:
		print("blastp failed")
		sys.exit()

	output = open(out,"r")
	sseq = open("subseq","w")
	for rows in output:
		col = rows.split("\t")
		sseq.write(col[1] + "\n")
	output.close()
	sseq.close()
	
#En el archivo sseq guardamos los subject resultantes del blast
#El objetivo es añadir las secuencias que aparezcan en la base de datos
#en el archivo final de blast
	
	cmd22= ['blastdbcmd', '-entry_batch', 'subseq', '-db', folder, '-outfmt', '%s', '-out', 'seq_list']
	try:
		call(cmd22)
	except:
		print("BlastP for looking sseq failed")
		sys.exit()

	fileseq = open("seq_list","r")
	sequence = list()
	for line1 in fileseq:
		sequence.append(line1)
	fileseq.close()

	final = "blastfinal"
	fileb = open(out,"r")
	finalfile = open(final,"w")
	a = 0
	for line2 in fileb:
		line2 = line2.strip()
		finalfile.write(line2 + "\t" + sequence[a])
		a += 1
	fileb.close()
	finalfile.close()
	

def finalblast(cov,identity,dicti):
	"""
	Creation of the final file of BlastP
	"""
	path = "results/"
	
	try:
		os.stat(path)
	except:
		os.mkdir(path)
	
	for key in dicti:
		f3 = path + key + ".fa"
		f4 = open(f3,"w")
		f4.write(">" + key + "\n" + dicti[key] + "\n")
		entry = open("blastfinal","r")
		for line in entry:
			fields = line.split("\t")
			if fields[0] == key:
				if float(fields[2]) >= float(cov) and float(fields[3]) >= float(identity):
					f4.write(">" + fields[1] + "\n" + fields[5] + "\n")
	f4.close()
	entry.close()
