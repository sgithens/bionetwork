from py2neo import node, rel, neo4j
conn = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

chem = conn.find('chemical',property_key="ChemicalID",property_value="MESH:C112297")
comp = list(chem)[0]

genelist = conn.find('gene',property_key="geneid",property_value="3784")

gene = list(genelist)[0]

comp.create_path("INTERACTION", gene)

# Adding a rel with properties (probably works)
# comp.create_path( ("INTERACTION", {'prop1':'val1','prop2':'val2'}), gene)
