from rdflib import Graph, plugin
from rdflib.serializer import Serializer

g=Graph().parse("../examples/hackair.jsonld", format="json-ld")
print(g.serialize(format='ttl'))


