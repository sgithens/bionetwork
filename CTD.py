#!/usr/bin/python

import os
import sys
import glob
import re
import csv
import pycurl
from py2neo import node, rel, neo4j, geoff

def infiles_check_gene():
	if os.path.exists('gene.geoff'):
		os.remove('gene.geoff')
	geofile = open('gene.geoff', 'w')
	genes_file= open('CTD_genes.csv','rb')
	genesf = csv.reader(genes_file, delimiter=',', quotechar='"')
	for row in genesf:
		geneval = "(" + row[2]+ " {\"geneid\":\"" + row[2] + "\" , \"GeneSymbol\":\"" + row[0] + \
			 "\" ,\"GeneName\":\"" + row[1] + "\" ,\"AltGeneIDs\":\"" + row[3] + "\" , \"Synonyms\":\"" + row[4] + \
			 "\" , \"BioGRIDIDs\":\"" + row[5] + "\" , \"PharmGKBIDs\":\"" + row[6] + "\" , \"UniprotIDs \":\"" + row[7] + "\" }) \n "
		geneval = unicode(geneval, errors='ignore')		
		geofile.write(geneval)
	geofile.close()
	genes_file.close()

def infiles_check_chem():
	if os.path.exists('chemical.geoff'):
		os.remove('chemical.geoff')
	geofile = open('chemical.geoff', 'w')	
	chem_file= open('CTD_chemicals.csv','rb')
	chemsf = csv.reader(chem_file, delimiter=',', quotechar='"')
	for row in chemsf:
		list=[]
                list = row[1].split(':')
                row[1] = ''.join(list)
		chemval = "(" + row[1]+ " {\"ChemicalID\":\"" + row[1] + "\" , \"ChemicalName\":\"" + row[0] + \
			 "\" ,\"CasRN\":\"" + row[2] + "\" ,\"Definition\":\"" + row[3] + "\" , \"ParentIDs\":\"" + row[4] + \
			 "\" , \"TreeNumbers\":\"" + row[5] + "\" , \"ParentTreeNumbers\":\"" + row[6] + "\" , \"Synonyms \":\"" + row[7] + "\" , \"DrugBankIDs\":\"" + row[8] + "\" })\n"
		chemval = unicode(chemval, errors='ignore')		
		geofile.write(chemval)
	geofile.close()
	chem_file.close()

def infiles_check_path():
	if os.path.exists('pathway.geoff'):
		os.remove('pathway.geoff')
	geofile = open('pathway.geoff', 'w')		
	path_file= open('CTD_pathways.csv','rb')
	pathf = csv.reader(path_file, delimiter=',', quotechar='"')
	for row in pathf:
		list=[]
                list = row[1].split(':')
                row[1] = ''.join(list)
		pathval = "(" + row[1]+ " {\"PathwayID\":\"" + row[1] + "\" , \"PathwayName\":\"" + row[0] + "\" })\n"		
		pathval = unicode(pathval, errors='ignore')		
		geofile.write(pathval)
	geofile.close()
	path_file.close()		

def infiles_check_dis():
	if os.path.exists('disease.geoff'):
		os.remove('disease.geoff')
	geofile = open('disease.geoff', 'w')		
	dis_file= open('CTD_diseases.csv','rb')
	disf = csv.reader(dis_file, delimiter=',', quotechar='"')
	for row in disf:
		list=[]
                list = row[1].split(':')
                row[1] = ''.join(list)
		disval = "(" + row[1]+ " {\"DiseaseID\":\"" + row[1] + "\" , \"DiseaseName\":\"" + row[0] + \
			 "\" ,\"Definition\":\"" + row[2] + "\" ,\"AltDiseaseIDs\":\"" + row[3] + "\" , \"ParentIDs\":\"" + row[4] + \
			 "\" , \"TreeNumbers\":\"" + row[5] + "\" , \"ParentTreeNumbers\":\"" + row[6] + "\" , \"Synonyms \":\"" + row[7] + "\" , \"SlimMappings\":\"" + row[8] + "\" })\n"		
		disval = unicode(disval, errors='ignore')
		geofile.write(disval)
	geofile.close()
	dis_file.close()		
'''
def load_graph_db_pycurl():
	curl -X 
'''

def main():
	infiles_check_gene()
	infiles_check_chem()
	infiles_check_path()
	infiles_check_dis()

if __name__ == "__main__":
	main()
