import nltk
from practnlptools.tools import Annotator
import re
import networkx as nx
ann=Annotator()


def shortDep(sent, e1, e2):
	"""
		return: shortest dependency path between e1 and e2
		format: ['E1', 'responded', 'fluids', 'E2']
	"""
#	print "sent: ", sent
#	print "e1 :", e1
#	sent = sent.replace('(','')
#	sent = sent.replace(')','')
	print e1,e2
	sent = sent.replace(e1, "Entity1",2)
	sent = sent.replace(e2, "Entity2",2)
#	tmpx = tagger.parse(sent)
#	sent_list,_,_,_,_ = zip(*tmpx)
	tmpy = ann.getAnnotations(sent)['pos']
	sent_list = zip(*tmpy)[0]
#	print sent_list
	e1_place = sent_list.index("Entity1") + 1
	e2_place = sent_list.index("Entity2") + 1
	
	dep_parse = ann.getAnnotations(sent, dep_parse=True)['dep_parse']
#	print dep_parse
	dp_list = dep_parse.split('\n')
	pattern = re.compile(r'.+?\((.+?), (.+?)\)')
	edges = []
	
	for dep in dp_list:
    		m = pattern.search(dep)
    		edges.append((m.group(1), m.group(2)))
#	print edges
	graph = nx.Graph(edges)  # Well that was easy
	s = "Entity1"+ "-" +str(e1_place)
	d = "Entity2"+ "-" +str(e2_place)

#	nx.shortest_path_length(graph, source=s, target=d)

	short_list = nx.shortest_path(graph, source=s, target=d) #['E1-6', 'responded-12', 'fluids-15', 'E2-19']
	short_sent = e1
	for w in short_list[1:-1]:
		short_sent += " "+w.split('-')[0]
	short_sent += " "+e2

	short_dep_list = short_sent.strip().split()
	return short_dep_list



#sent = "Co-administration of probenecid with acyclovir has been shown to increase the mean half-life and the area under the concentration-time curve"
sent = "When administered concurrently, the following drugs may interact with amphotericinB : Antineoplasticagents : may enhance the potential for renal toxicity, bronchospasm and hypotension."
#print "shortest path(prbenecid, acyclotvir)", shortDep(sent, 'probenecid', 'acyclovir')

print "shortest path(prbenecid, acyclotvir)", shortDep(sent, 'amphotericinB', 'Antineoplasticagents')












