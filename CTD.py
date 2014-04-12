#!/usr/bin/python

import os
import sys
import glob
import re
import csv
import requests
#from py2neo import node, rel, neo4j, geoff
#import json

def file_exists_geoff(file):
	if os.path.exists(file):
		os.remove(file)
	global geofile
	geofile = open(file, 'w')

def infiles_check_gene(files,csvfile):
	file_exists_geoff(files)
	genes_file= open(csvfile,'rb')
	genesf = csv.reader(genes_file, delimiter=',', quotechar='"')
	for row in genesf:
		uniqid = row[2]
		geneval = "(" + uniqid + ":gene!geneid {\"geneid\":\"" + row[2] + "\" , \"GeneSymbol\":\"" + row[0] + \
			 "\" ,\"GeneName\":\"" + row[1] + "\" ,\"AltGeneIDs\":\"" + row[3] + "\" , \"Synonyms\":\"" + row[4] + \
			 "\" , \"BioGRIDIDs\":\"" + row[5] + "\" , \"PharmGKBIDs\":\"" + row[6] + "\" , \"UniprotIDs \":\"" + row[7] + "\" })\n "
		uniquelist.append(['genes',uniqid, row[2]])
		geneval = unicode(geneval, errors='ignore')		
		geofile.write(geneval)
	geofile.close()
	genes_file.close()

def infiles_check_chem(files,csvfile):
	file_exists_geoff(files)	
	chem_file= open(csvfile,'rb')
	chemsf = csv.reader(chem_file, delimiter=',', quotechar='"')
	for row in chemsf:
        	list = row[1].split(':')
        	uniqid = '_'.join(list)
		chemval = "(" + uniqid + ":chemical!ChemicalID {\"ChemicalID\":\"" + row[1] + "\" , \"ChemicalName\":\"" + row[0] + \
			 "\" ,\"CasRN\":\"" + row[2] + "\" ,\"Definition\":\"" + row[3] + "\" , \"ParentIDs\":\"" + row[4] + \
			 "\" , \"TreeNumbers\":\"" + row[5] + "\" , \"ParentTreeNumbers\":\"" + row[6] + "\" , \"Synonyms \":\"" + row[7] + "\" , \"DrugBankIDs\":\"" + row[8] + "\" })\n"
		uniquelist.append(['chemicals',uniqid, row[1]])
		chemval = unicode(chemval, errors='ignore')		
		geofile.write(chemval)
	geofile.close()
	chem_file.close()

def infiles_check_path(files,csvfile):
	file_exists_geoff(files)	
	path_file= open(csvfile,'rb')
	pathf = csv.reader(path_file, delimiter=',', quotechar='"')
	for row in pathf:
        	list = row[1].split(':')
        	uniqid = '_'.join(list)
		pathval = "(" + uniqid + ":pathway!PathwayID {\"PathwayID\":\"" + row[1] + "\" , \"PathwayName\":\"" + row[0] + "\" })\n"		
		uniquelist.append(['pathway',uniqid, row[1]])
		pathval = unicode(pathval, errors='ignore')		
		geofile.write(pathval)
	geofile.close()
	path_file.close()		

def infiles_check_dis(files,csvfile):
	file_exists_geoff(files)	
	dis_file= open(csvfile,'rb')
	disf = csv.reader(dis_file, delimiter=',', quotechar='"')
	for row in disf:
        	list = row[1].split(':')
        	uniqid = '_'.join(list)
		disval = "(" + uniqid + ":disease!DiseaseID {\"DiseaseID\":\"" + row[1] + "\" , \"DiseaseName\":\"" + row[0] + \
			 "\" ,\"Definition\":\"" + row[2] + "\" ,\"AltDiseaseIDs\":\"" + row[3] + "\" , \"ParentIDs\":\"" + row[4] + \
			 "\" , \"TreeNumbers\":\"" + row[5] + "\" , \"ParentTreeNumbers\":\"" + row[6] + "\" , \"Synonyms \":\"" + row[7] + "\" , \"SlimMappings\":\"" + row[8] + "\" })\n"		
		uniquelist.append(['disease',uniqid, row[1]])
		disval = unicode(disval, errors='ignore')
		geofile.write(disval)
	geofile.close()
	dis_file.close()		

def load_graph_db_pycurl(files):
	print ("Loading file " + files + "into GraphDB")
	geosfile = open(files, 'rb')	
	readgene = geosfile.readlines()
	geosfile.close()
	for lines in readgene:
		url = 'http://localhost:7474/load2neo/load/geoff'
		r = requests.post(url, data=lines)
'''
def load_graph_dbfiles_pycurl():
        geofile = open('chemical.geoff', 'rb')
        url = 'http://localhost:7474/load2neo/load/geoff'
        r = requests.post(url, data=geofile)
	print r.status_code
'''

def ctdmain():

	global uniquelist
	uniquelist = []
	csv_file = ['../csv/CTD_chemicals.csv','../csv/CTD_diseases.csv','../csv/CTD_pathways.csv','../csv/CTD_genes.csv']
	geoff_file = ['chemical.geoff','disease.geoff','pathway.geoff','gene.geoff']
	infiles_check_chem(geoff_file[0],csv_file[0])
	infiles_check_dis(geoff_file[1],csv_file[1])
	infiles_check_path(geoff_file[2],csv_file[2])
	infiles_check_gene(geoff_file[3],csv_file[3])

	if os.path.exists('uniqueids_file'):
		os.remove('uniqueids_file')
	uniqfile = open('uniqueids_file', 'w')
	
	for items in uniquelist:
		line = ','.join(items)
		uniqfile.write(str(line) + '\n')
	uniqfile.close()

	for files in geoff_file:
		load_graph_db_pycurl(files)

if __name__ == "__main__":
	ctdmain()
