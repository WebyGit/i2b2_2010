import networkx as nx
import numpy as np
import sys
import re
from practnlptools.tools import Annotator
ann=Annotator()

def preProcess(sent):
	sent = sent.lower()
	sent = sent.replace('(', 'leftbracket')
	sent = sent.replace(')', 'rightbracket')
	sent = re.sub('\d', 'dg',sent)
	tmp = ann.getAnnotations(sent)['pos']
	sent,_ = zip(*tmp)
	sent = ' '.join(sent)
	return sent

def readData(ftrain):
  fp = open(ftrain, 'r')
  samples = fp.read().strip().split('\n\n\n')
  sent_names     = []		#1-d array 
  sent_lengths   = []		#1-d array
  sent_contents  = []		#2-d array [[w1,w2,....] ...]
  sent_lables    = []		#1-d array
  entity1_list   = []		#2-d array [[e1,e1_s,e1_e,e1_t] [e1,e1_s,e1_e,e1_t]...]
  entity2_list   = []		#2-d array [[e1,e1_s,e1_e,e1_t] [e1,e1_s,e1_e,e1_t]...]
  for sample in samples:
	name, sent, entities, relation = sample.strip().split('\n')	
	
	ma = re.match(r"\[['\"](.*)['\"], '(.*)', ['\"](.*)['\"]\]", relation.strip())
	if(ma):
		lable = ma.group(2)		
	elif relation == '[0]':
		lable = 'other'
	else:
		print "Error in reading", relation
		exit(0)
	if (lable == 'TrWP' or lable == 'TrNAP' or lable == 'TrIP'):
		continue
	sent_lables.append(lable)
	sent = preProcess(sent)
	sent_lengths.append(len(sent.split()))
	sent_names.append(name)
	
	sent_contents.append(sent)

	m = re.match(r"\(\[['\"](.*)['\"], (\d*), (\d*), '(.*)'\], \[['\"](.*)['\"], (\d*), (\d*), '(.*)'\]\)", entities.strip())
	if m :
		e1   = m.group(1)
		e1 = preProcess(e1)

		e1_s = int(m.group(2))
		e1_e = int(m.group(3))
		e1_t = m.group(4)

		e2   = m.group(5) 
		e2 = preProcess(e2)
		e2_s = int(m.group(6))
		e2_e = int(m.group(7))
		e2_t = m.group(8)
		if(e1_s < e2_s):
			entity1_list.append([e1,e1_s,e1_e,e1_t])
			entity2_list.append([e2,e2_s,e2_e,e2_t])
		else:
			entity1_list.append([e2,e2_s,e2_e,e2_t])
			entity2_list.append([e1,e1_s,e1_e,e1_t])
#		print e1,e2
	else:
		print "Error in readign", entities.strip()
#		exit(0)	
  return sent_contents,entity1_list, entity2_list, sent_lables 

def makeDistance(sent, e1, e2):
	sent = sent.split() 
 	entity1, entity1_s, entity1_e, entity1_t  = e1
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

	entity2, entity2_s, entity2_e, entity2_t  = e2 	
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

def shortDep(sent, e1, e2):
 	entity1, entity1_s, entity1_e, entity1_t  = e1
	entity2, entity2_s, entity2_e, entity2_t  = e2
 	sent = sent.replace(entity1, "Entity1",2)
	sent = sent.replace(entity2, "Entity2",2)
 
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
	 
def makeFeatures(sent_contents, entity1_list, entity2_list, sent_lables):
	sent_list = []
	pos_list = []
	chunk_list = []
	dep_parse_list = []
	d1_list = []
	d2_list = []
	type_list = []
	
	for sent, e1, e2, lable in zip(sent_contents, entity1_list, entity2_list, sent_lables):		
		tmpy = ann.getAnnotations(sent)
		_, pos = zip(*tmpy['pos']) 		 
		_,chunk = zip(*tmpy['chunk'])		 		
		d1, d2, t = makeDistance(sent, e1, e2)
		short_dep, short_dep_feature = shortDep(sent, e1, e2)

		d1_list.append(d1)
		d2_list.append(d2)
		type_list.append(t)
		sent_list.append(sent)
		pos_list.append(pos)
		chunk_list.append(chunk)
		dep_parse_list.append(short_dep_feature)

	return sent_list, pos_list, chunk_list, d1_list, d2_list, type_list, dep_parse_list

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

def makePaddedListSent(sent_list, pad_symbol= '<pad>'):
	maxl = max([len(sent.split()) for sent in sent_list])
	T = []
 	for sent in sent_list:
#		print sent
		t = []
		lenth = len(sent.split())
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



