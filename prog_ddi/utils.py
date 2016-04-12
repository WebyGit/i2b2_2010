import networkx as nx
import numpy as np
import sys
import re
from practnlptools.tools import Annotator
ann=Annotator()

def preProcess(sent):
	sent = sent.lower()	
	tmp = ann.getAnnotations(sent)['pos']
	sent,_ = zip(*tmp)
	sent = ' '.join(sent)
	sent = sent.replace('(', 'leftbracket')
	sent = sent.replace(')', 'rightbracket')
	sent = re.sub('\d', 'dg',sent)
	
	return sent

#When ertapenem is co-administered with probenecid (500 mg p.o. every 6 hours), probenecid competes for active tubular secretion and reduces the renal clearance of ertapenem.
#ertapenem|drug||false|none||probenecid|drug


def readData(ftrain):

  	fp = open(ftrain, 'r')
	samples = fp.read().strip().split('\n\n')
	sent_list = []
	e1_list = []
	e2_list = []
	rel_list = []
	for sample in samples:
		sent, ent = sample.strip().split('\n')
		sent = preProcess(sent)
		e1_part,rel_part,e2_part = ent.split('||')
		e1, t1 = e1_part.split('|')
		e1 = preProcess(e1)	
		e2, t2,= e2_part.split('|')
		e2 = preProcess(e2)
		rel, rel_type = rel_part.split('|')
		sent_list.append(sent)
		e1_list.append([e1,t1])
		e2_list.append([e2,t2])
		rel_list.append([rel, rel_type])
	return sent_list, e1_list, e2_list, rel_list

def shortDep(sent, e1, e2):

 	entity1, entity1_t  = e1
	entity2, entity2_t  = e2
	sent = sent.replace(entity1, "Entity1",1)
	sent = sent.replace(entity2, "Entity2",1)
 
	dep_parse = ann.getAnnotations(sent, dep_parse=True)['dep_parse']
	tmp = ann.getAnnotations(sent, dep_parse=True)['pos']
	tmp1,_ = zip(*tmp)
	
	s1 = tmp1.index('Entity1')
	s2 = tmp1.index('Entity2')

	dp_list = dep_parse.split('\n')
	pattern = re.compile(r'.+?\((.+?), (.+?)\)')
	edges = []
 	for dep in dp_list:
    		m = pattern.search(dep)
    		edges.append((m.group(1), m.group(2)))
	graph = nx.Graph(edges)   
	s = "Entity1"+ "-" +str(s1+1)
	d = "Entity2"+ "-" +str(s2+1)

	short_list = nx.shortest_path(graph, source=s, target=d) #['E1-6', 'responded-12', 'fluids-15', 'E2-19']
	short_sent = entity1
	for w in short_list[1:-1]:
		w = w.split('-')
		w = '-'.join(w[0:-1])
		short_sent += " "+w
	short_sent += " "+entity2
	short_dep_list = short_sent.strip().split()
	  
	sent = sent.replace("Entity1", entity1, 2)
	sent = sent.replace("Entity2", entity2, 2)

	sent = sent.split()
 	list1 = [False for w in sent]
 	for w in short_dep_list:
 		ind = sent.index(w)
		list1[ind] = True		
	return short_dep_list, list1


def makeFeatures(sent_lista, e1_lista, e2_lista, rel_lista):
#	print 'sunil'
	sent_list = []
	pos_list = []
	chunk_list = []
	dep_parse_list = []
	d1_list = []
	d2_list = []
	type_list = []
	lable_list = []
	for sent, e1, e2, rel in zip(sent_lista, e1_lista, e2_lista, rel_lista):
		tmpy = ann.getAnnotations(sent)
		_, pos = zip(*tmpy['pos']) 
		_,chunk = zip(*tmpy['chunk'])
		d1, d2, t = makeDistance(sent, e1, e2)
		short_dep, short_dep_feature = shortDep(sent, e1, e2)
 
		sent = sent.split()
		t1 = []; t2 = []; t3 = []; t4 = []; t5 = [];
		for word in short_dep:
			index = sent.index(word)		
			t1.append(pos[index])
			t2.append(chunk[index])
			t3.append(d1[index])
			t4.append(d2[index])
			t5.append(t[index])
		sent_list.append(short_dep)
		pos_list.append(t1)
		chunk_list.append(t2)
		d1_list.append(t3)
		d2_list.append(t4)
		type_list.append(t5)
 		if rel[0] == 'false':
			lable_list.append('other')
		else :
			lable_list.append(rel[1])

	return sent_list, pos_list, chunk_list, d1_list, d2_list, type_list, lable_list 

def makeDistance(sent, e1, e2):
	sent = sent.split() 
 	entity1, entity1_t  = e1
 	sent_length = len(sent)
	e1 = entity1.split() 
	s1_p = sent.index(e1[0])
	e1_p = sent.index(e1[-1]) 

	t = [ 'O' for w in sent]
	d1 = []
	for i in range(sent_length):
		if i < s1_p :
			d1.append(str(i - s1_p))
			 
		elif i > e1_p :
			d1.append(str(i - e1_p))
			 
		else:
			d1.append('0')
	 		t[i]= entity1_t

	entity2, entity2_t  = e2 	
	e2 = entity2.split()
	s2_p = sent.index(e2[0])
	e2_p = sent.index(e2[-1])
	d2 = []
	for i in range(sent_length):
		if i < s2_p :
			d2.append(str(i - s2_p))
			
		elif i > e2_p :
			d2.append(str(i - e2_p))
		else:
			d2.append('0')
			t[i] = entity2_t

#	print len(sent), len(sent_l), len(d1), len(d2), len(t)
	return d1, d2, t

def makePaddedList(sent_contents, pad_symbol= '<pad>'):
	maxl = max([len(sent) for sent in sent_contents])
	T = []
 	for sent in sent_contents:
		t = []
		lenth = len(sent)
		for i in range(lenth):
			t.append(sent[i])
		for i in range(lenth,maxl):
			t.append(pad_symbol)
		T.append(t)	

	return T

def makeWordList(sent_list):
	wf = {}
	for sent in sent_list:
		for w in sent:
 			if w in wf:
				wf[w] += 1
			else:
				wf[w] = 0
	wl = {}
	i = 0
	for w,f in wf.iteritems():
		wl[w] = i
		i += 1
	return wl

def makeLableList(lable_list):
	wf = {}
	for w in lable_list:
		if w in wf:
			wf[w]+=1
		else:
			wf[w] = 0
	wl = {}
	i = 0
	for w,f in wf.iteritems():
		wl[w] = i
		i += 1
	return wl


def mapWordToId(sent_contents, word_dict):
	T = []
	for sent in sent_contents:
		t = []
		for w in sent:
			t.append(word_dict[w])
		T.append(t)
	return T


def mapLabelToId(sent_lables, label_dict):
	return [label_dict[label] for label in sent_lables]


