"""graphml/Entity Relationship to JSON Schema

Usage: 

$ python graphml2jsch.py graphmlfile

The JSON schema is written into graphmlfile_schema.json

!! requires python 3.7 (uses type annotations)
 
This scripts takes as input a graphml file produced with the yEd graph editor
that contains 'Entity with Attributes' nodes and labelled edges. It translates it
into a JSON Schema that is compatible with JSON-LD.

The translation rules are:

- every 'Entity with Attributes' node with label CCC and links LL1, LL2, ... to
nodes CC1, CC2, ... , and superclasses SC1, SC2, ... is transformed into an 
object definition of the form


"CCC": {
   "allOf": [
      { "$ref": "#/$defs/SC1" },   
      ...
      {"properties": {
         "@id": {"type": "string"},      <---- for compatibility with JSON-LD
         "@type": {"type": "string"}     <---- for compatibility with JSON-LD
         ,"LL1": {"$ref": "#/$defs/CC1_"}
         ,"LL2": {"$ref": "#/$defs/CC2_"}
         ...
      },
      "additionalProperties": false      <---- no other property allowed
      }
   ]
}


and an object or object list definition of the form

"CCC_": {
   "oneOf": [
      {"type": "array", "items": {"$ref": "#/$defs/CCC"}},
      {"$ref": "#/$defs/CCC"}]
}

So, when a property must have a value of type T it can be either a single T object 
or a list of objects of type T

- if the entity has no subclass, no superclass and no edge pointing to another entity 
(e.g. ExternalID, DatasetName, YearOfBirth, ...), it is consisered as "literal" and 
equivalent to string. So its definition is 

"CCC": {
   "type": "string" },



G. Falquet 2019

"""
import xml.etree.ElementTree as ET
import re
import sys
import urllib.parse
from typing import List, FrozenSet, Dict, Tuple

ns = {'g': 'http://graphml.graphdrawing.org/xmlns',
      'x': 'http://www.yworks.com/xml/yfiles-common/markup/2.0',
      'y': 'http://www.yworks.com/xml/graphml'}


# usage = python graphml2owl.py file.graphml
ifileName = sys.argv[1]
ofileName = sys.argv[1]+"_schema.json"
print('Output to '+ofileName)
sys.stdout = open(ofileName, 'w')


root: ET.Element = ET.parse(ifileName).getroot()


classNames: FrozenSet[str] = frozenset()
classNameOfNode: Dict[str, str] = {}
annotationOfClass: Dict[str, str] = {}
edgesFromClass: Dict[str, FrozenSet[str]] = {}
edgesToClass: Dict[str, FrozenSet[str]] = {}
subClassOf: Dict[str,FrozenSet[str]] = {}
propertiesOf: Dict[str,Dict[str,FrozenSet[str]]] = {}

# algo
#
# for each node
#    
for n in root.findall('.//g:node',ns):
    nodeLabels: List[ET.Element] = n.findall('./g:data/y:GenericNode[@configuration="com.yworks.entityRelationship.big_entity"]/y:NodeLabel',ns)
    
    if len(nodeLabels) > 0 :
        clsLabel: ET.Element = nodeLabels[0]
        nodeId = n.get('id')
        clsName = clsLabel.text
        clsName = re.sub(r'[^a-z^A-Z^0-9^-^:]', '_', clsName)
        classNames = classNames.union({clsName})
        classNameOfNode[nodeId] = clsName
        if len(nodeLabels) > 1 :
            annotLabel = nodeLabels[1]
            if annotLabel.text.strip() != "" :
                annotationOfClass[clsName] = annotLabel.text
        # print(clsName, nodeId)


for e in root.findall('.//g:edge',ns) :
   src = e.get("source")
   tgt = e.get("target")
   edgeLabel: ET.Element = e.find(".//y:EdgeLabel",ns)
   label = "UNDEF_Property"

   if edgeLabel != None : label = edgeLabel.text 

   restrictionType = 'owl:allValuesFrom'
   #  edge labels of the form 'propertyName min 1' 
   if len(re.findall(r' min 1$', label)) > 0 :
       label = re.sub(r' min 1$', '', label)
       restrictionType = 'owl:someValuesFrom'

   label = re.sub(r'[^a-z^A-Z^0-9^-^:]', '_', label)
   
   if ((src in classNameOfNode ) and (tgt in classNameOfNode)) :
       srcname = classNameOfNode[src]
       tgtname = classNameOfNode[tgt]
       if label.lower() == "subclassof" :
            if srcname not in subClassOf : 
                subClassOf[srcname] = frozenset()
            subClassOf[srcname] = subClassOf[srcname].union({tgtname})
            # print(":"+classNameOfNode[src]+"  rdfs:subClassOf  :"+classNameOfNode[tgt]+"  .")
       else :
            if srcname not in propertiesOf :
                propertiesOf[srcname] = {}
            if label not in propertiesOf[srcname] :
                propertiesOf[srcname][label] = frozenset()
            propertiesOf[srcname][label] = propertiesOf[srcname][label].union({tgtname})
        #    print(":"+classNameOfNode[src]+"  rdfs:subClassOf  ")
        #    print("       [a owl:Restriction ; owl:onProperty :"+label+" ; "+restrictionType+"  :"+classNameOfNode[tgt]+"]  .")
           
#   else :
#        print("## edge between non-class nodes: "+label)

print("""
{
"$schema": "http://json-schema.org/draft-06/schema#",

"$defs": {

""")

firstDef = True

for c in classNames : 
    if not firstDef :
        print(",")
    else:
        firstDef = False

    print('"'+c+'": {')
    if c in annotationOfClass : print('   "$comment": "'+annotationOfClass[c]+'",')
    
    if (c not in subClassOf) and (c not in propertiesOf) :
        print('"type": "string" },')
    else:
        print('   "allOf": [')

        if c in subClassOf :
            for d in subClassOf[c]:
                print('      { "$ref": "#/$defs/'+d+'" },')

        print(
"""      {"type": "object",
       "properties": {
        "@id": {"type": "string"},
        "@type": {"type": "string"}
""")
        if c in  propertiesOf: 
            for p in propertiesOf[c] :
                # check if the same property appears twice or more
                if len(propertiesOf[c][p]) == 1:
                    for t in propertiesOf[c][p] :
                        print('         ,"'+p+'": {"$ref": "#/$defs/'+t+'_"}')
                else: 
                    print('         ,"'+p+'": {"oneOf": [')
                    sep = ' '
                    for t in propertiesOf[c][p] :
                        print('             '+sep+'{"$ref": "#/$defs/'+t+'"}')
                        sep = ','
                    print('             '+sep+'{"type": "array", "items": {"oneOf": [')
                    sep = ''
                    for t in propertiesOf[c][p] :
                        print('                 '+sep+'{"$ref": "#/$defs/'+t+'"}')
                        sep = ','
                    print('             ]}}')
                    print('         ]}')
        print('      },')
        print('      "additionalProperties": false')
        print('      }')
        print('   ]')
        print('},')

    print()
    print('"'+c+'_": {')
    print('   "oneOf": [')
    print('      {"type": "array", "items": {"$ref": "#/$defs/'+c+'"}},')
    print('      {"$ref": "#/$defs/'+c+'"}]')
    print('}')

print(',')
print('"CSObject": {"anyOf" : [')
sep = '   '
for c in classNames : 
   print(sep+'{"$ref": "#/$defs/'+c+'"}')
   sep = '   ,'
print('   ]')
print('}')


print('}') # end of definition

print()
print(",")
print('"type": "array",')
print('"items": {"$ref": "#/$defs/CSObject"}')

print('}')





sys.stdout.flush()
sys.stdout.close()
