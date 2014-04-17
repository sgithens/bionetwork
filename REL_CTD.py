#!/usr/bin/python
import os
import sys
import csv
import requests

def file_exists_geoff(filez):
	if os.path.exists(filez):
		os.remove(filez)
	global geofile
	geofile = open(filez, 'wb')

def line_file_geoff(row,reltype):

	if reltype == 0:
		uniqid = row[1].replace(":","_")
		ctdval = "(" + uniqid + ":chemical!ChemicalID {\"ChemicalID\":\"" + row[1] + "\" , \"ChemicalName\":\"" + row[0] + \
			 "\" ,\"CasRN\":\"" + row[2] + "\" ,\"Definition\":\"" + row[3] + "\" , \"ParentIDs\":\"" + row[4] + \
			 "\" , \"TreeNumbers\":\"" + row[5] + "\" , \"ParentTreeNumbers\":\"" + row[6] + "\" , \"Synonyms \":\"" + row[7] + "\" , \"DrugBankIDs\":\"" + row[8] + "\" })\n"
		return ctdval
	elif reltype == 1:
		uniqid = row[1].replace(":","_")
		ctdval = "(" + uniqid + ":disease!DiseaseID {\"DiseaseID\":\"" + row[1] + "\" , \"DiseaseName\":\"" + row[0] + \
			 "\" ,\"Definition\":\"" + row[2] + "\" ,\"AltDiseaseIDs\":\"" + row[3] + "\" , \"ParentIDs\":\"" + row[4] + \
			 "\" , \"TreeNumbers\":\"" + row[5] + "\" , \"ParentTreeNumbers\":\"" + row[6] + "\" , \"Synonyms \":\"" + row[7] + "\" , \"SlimMappings\":\"" + row[8] + "\" })\n"			  
		return ctdval
	elif reltype == 2:
		uniqid = row[1].replace(":","_")	  
		ctdval = "(" + uniqid + ":pathway!PathwayID {\"PathwayID\":\"" + row[1] + "\" , \"PathwayName\":\"" + row[0] + "\" })\n"		
		return ctdval		
	elif reltype == 3:
		uniqid = row[2]
		ctdval = "(" + uniqid + ":gene!geneid {\"geneid\":\"" + row[2] + "\" , \"GeneSymbol\":\"" + row[0] + \
			 "\" ,\"GeneName\":\"" + row[1] + "\" ,\"AltGeneIDs\":\"" + row[3] + "\" , \"Synonyms\":\"" + row[4] + \
			 "\" , \"BioGRIDIDs\":\"" + row[5] + "\" , \"PharmGKBIDs\":\"" + row[6] + "\" , \"UniprotIDs \":\"" + row[7] + "\" })\n "
		return ctdval
	elif reltype == 4:
	  	ctdval = "(MESH_"+ row[1] +")-[:CGINTERACTS! {\"Organism\":" + row[6] +", \"OrganismID\":"+ row[7] + \
			", \"Interaction\":"+ row[8] +", \"InteractionActions\":" +row[9]+ ", \"PubMedIDs\":"+ row[10] +"}]->("+ row[4] +")"
		ctdval = unicode(ctdval, errors='ignore')
		return ctdval		
	elif reltype == 5:
		uniqid = row[4].replace(":","_")
		ctdval = "(MESH_"+ row[1] +")-[:CDINTERACTS! {\"DirectEvidence\":" + row[5] +", \"InferenceGeneSymbol\":"+ row[6] +  \
			", \"InferenceScore\":"+ row[7] +", \"OmimIDs\":" +row[8]+ ", \"PubMedIDs\":"+ row[9] +"}]->("+ uniqid +")"
		return ctdval			
	elif reltype == 6:
		uniqid = row[4].replace(":","_")
		ctdval = "(MESH_"+ row[1] +")-[:CPINTERACTS! {\"PValue\":" + row[5] +", \"CorrectedPValue\":"+ row[6] +  \
			", \"TargetMatchQty\":"+ row[7] +", \"TargetTotalQty\":" +row[8]+ ", \"BackgroundMatchQty\":"+ row[9] + \
			", \"BackgroundTotalQty\":"+ row[10] +"}]->("+ uniqid +")"
		return ctdval			
	elif reltype == 7:
		firstnode=row[1].replace(":","_")
		secondnode=row[3].replace(":","_")
		ctdval = "("+ firstnode +")-[:DPINTERACTS! {\"InferenceGeneSymbol\":" + row[4] +"}]->("+ secondnode +")"		
		return ctdval		
	elif reltype == 8:
		uniqid=row[3].replace(":","_")
		ctdval = "("+ row[1] +")-[:GDINTERACTS! {\"DirectEvidence\":" + row[4] +", \"InferenceChemicalName\":"+ row[5] +  \
			", \"InferenceScore\":"+ row[6] +", \"OmimIDs\":" +row[7]+ ", \"PubMedIDs\":"+ row[8] +"}]->("+ uniqid +")"
		return ctdval			
	elif reltype == 9:
		uniqid=row[3].replace(":","_")
		ctdval = "("+ row[1] +")-[:GPINTERACTS!]->("+ uniqid +")"
		return ctdval		
	else:
		printf("Default Statement\n");

def infiles_check_ctd(files,csvfile,num):
	global ctdval
	file_exists_geoff(files)	
	ctdfile= open(csvfile,'rb')
	ctdf = csv.reader(ctdfile, delimiter=',', quotechar='"')
	for row in ctdf:
		ctdval = line_file_geoff(row,num)
		geofile.write(ctdval)
	geofile.close()
	ctdfile.close()		

def load_graph_db_pycurl(files):
	print ("Loading file " + files + " into GraphDB")
	geosfile = open(files, 'rb')	
	readgene = geosfile.readlines()
	for lines in readgene:
		url = 'http://localhost:7474/load2neo/load/geoff'
		r = requests.post(url, data=lines)
	geosfile.close()

def ctdmain():
	csv_file = ['../csv/CTD_chemicals.csv','../csv/CTD_diseases.csv','../csv/CTD_pathways.csv','../csv/CTD_genes.csv', '../csv/CTD_chem_gene_ixns.csv', \
				'../csv/CTD_chemicals_diseases.csv','../csv/CTD_chem_pathways_enriched.csv', '../csv/CTD_diseases_pathways.csv', '../csv/CTD_genes_diseases.csv', \
				'../csv/CTD_genes_pathways.csv']
	geoff_file = ['chemical.geoff','disease.geoff','pathway.geoff','gene.geoff','chemgen.geoff','chemdis.geoff', \
				'chempath.geoff','dispath.geoff','gendis.geoff','genpath.geoff']
	for i in range(len(geoff_file)):
		infiles_check_ctd(geoff_file[i],csv_file[i], i)
	for files in geoff_file:
		load_graph_db_pycurl(files)

if __name__ == "__main__":
	ctdmain()