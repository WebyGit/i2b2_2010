import numpy as np
import nltk
from practnlptools.tools import Annotator
import re
import networkx as nx
#from geniatagger import GeniaTagger
#tagger = GeniaTagger('/home/sunilitggu/python_pack/geniatagger-3.0.2/geniatagger')

ann=Annotator()

#He was noted to have an erythematous perianal rash and for this was started on Nystatin powder . ||| c="nystatin powder" 64:15 64:16||r="TrAP"||c="an erythematous perianal rash" 64:5 64:8 ||| record-107.txt
#3. Apnea and bradycardia of prematurity . ||| c="prematurity" 91:5 91:5||r="PIP"||c="bradycardia" 91:3 91:3 ||| record-107.txt

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
	wl['unkown'] = 0	
	for w,f in wf.iteritems():
		i += 1
		wl[w] = i
	return wl

def makeRelList(rel_list):
	rel_dict = {}
 	for rel in rel_list:
		if rel in rel_dict:
			rel_dict[rel] += 1
		else:
			rel_dict[rel] = 0
	wl = {}
	i = 0
 	for w,f in rel_dict.iteritems():
		wl[w] = i
		i += 1
	return wl 					

def readWordList(fname):
	with open(fname) as f:
		wl={}
		wl['unkown'] = 0
		i = 0
		for line in f:
			i += 1 
			line = line.strip()
			wl[line] = i
		f.close()
	return wl

def readDataThroughGenia(fname):
	"""
	s1 : (int) entity one start place
	e1 : (int) entity one end place
	s2 : (int) entity two start place
	e2 : (int) entity two end place
	entity1 : (string) first entity in sentence
	entity2 : (string) sencond entity in sentence
	rel: (string) relation name ig. TrAP = (e1,e2), TrAP_r = (e2,e1)
	sent: sentence list
	"""
	with open(fname) as f:
		sent_list = []
		pos_list = []
		chunk_list = []
		short_dep_list = []
		entity1_list = []
		entity2_list = []
 		rel_list = []		
		for line in f:	
			line = line.replace('(','')
			line = line.replace(')','')		 
			line = line.lower()
			sent,rel_part = line.strip().split("|||")[0:2]			
			tags = tagger.parse(sent)
			sent_t,sent_o, sent_pos, sent_chunk, sent_bio = zip(*tags)
			sent_list.append(sent_t)
  			if(len(sent_pos) == len(sent_t)):
				pos_list.append(sent_pos)
			else:
				print "pos and sent lenth not matching"
				print zip(sent_t,sent_l)
				print sent_l
				print sent_t
				exit(0)

			#chunking
			if(len(sent_chunk) == len(sent_t)):
				chunk_list.append(sent_chunk)
			else:								
				print "chunk and sen length not matching"				 
				print sent_chunk
				print sent_l
				exit(0)
			
			
			tmp = rel_part.strip().split("||")
			e1 = tmp[0].partition('"')[-1].rpartition('"')[0]
			e1_s = int(tmp[0].strip().split()[-2].split(':')[1])
			e1_e = int(tmp[0].strip().split()[-1].split(':')[1])
			r = tmp[1].partition('"')[-1].rpartition('"')[0]
			e2 = tmp[2].partition('"')[-1].rpartition('"')[0]
			e2_s = int(tmp[2].strip().split()[-2].split(':')[1])
			e2_e = int(tmp[2].strip().split()[-1].split(':')[1])

			if ( e1_s < e2_s ) :
				entity1 = e1
				entity2 = e2
 				rel = r
			else:		
				entity1 = e2
				entity2 = e1
 				rel = r	+ "_r"

			entity1_list.append(entity1)	 
			entity2_list.append(entity2)
 			rel_list.append(rel)
			print sent
			short_dep = shortDep(sent, entity1, entity2)
			short_dep_list.append(short_dep)

		f.close()
	return sent_list, pos_list, chunk_list, short_dep_list, entity1_list, entity2_list, rel_list


#He was noted to have an erythematous perianal rash and for this was started on Nystatin powder . ||| c="nystatin powder" 64:15 64:16||r="TrAP"||c="an erythematous perianal rash" 64:5 64:8 ||| record-107.txt

#TrAP = (e1, e2)
#TrAP_ = (e2, e1)




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

	
def pad_sentences(sentences, padding_word='<pad>'):
    """
    Pads all sentences to the same length. The length is defined by the longest sentence.
    Returns padded sentences.
    """
    sequence_length = max(len(x[0]) for x in sentences)
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i][0]
        num_padding = sequence_length - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences, sequence_length


def relCount(sents):
 	y = []
	for sent in sents:
		rel = sent[1]
		y.append(rel) 
	return y


def creatDict(pos):
	tag_dict = {}
	i = 0
	for tags in pos:
		for tag in tags:
			if not tag in tag_dict:
				tag_dict[tag] = i
				i += 1
	return tag_dict

def wordPosMapping(sents, wordlist, lables):
	"""
		returns: X_train : 2dim array with Nxd where d is length of largest sentence 
			 Y_train : NXm where m is number of lebles 
			 d1 : Nxd of for every sentence of every word distance from e1
			 d2 : Nxd for every sentence of every word distance from e2
	"""
	padded_sents, maxl = pad_sentences(sents)
	X_train = [] #Sentence only with padding
	for sent in padded_sents:
		x = []
		for word in sent:
			if word in wordlist:
				x.append(word)
			else:
				x.append("unkown")
		X_train.append(x)

	y = [lables[sent[1]] for sent in sents] #lables only
	d1 = [] #distance from first entity e1
	d2 = [] #distance from second entity e2
	for sent in sents:		
		e1_s = int(sent[3])
		e1_e = int(sent[4])
		e2_s = int(sent[6])
		e2_e = int(sent[7])
		t1 = []
		t2 = []
		for i in range(maxl):
			if i < e1_s :
				t1.append( i - e1_s )
			elif i > e1_e :
				t1.append( i - e1_e )
			else:
				t1.append(0)

		for i in range(maxl):
			if i < e2_s :
				t2.append( i - e2_s )
			elif i > e2_e :
				t2.append( i - e2_e )
			else:
				t2.append(0)
		d1.append(t1)
		d2.append(t2)

	#Create training datset formate
	X_t = np.array([[wordlist[word] for word in sent] for sent in X_train])
	

	pos = [[t for w,t in nltk.pos_tag(s)] for s in X_train]
	print "len pos", len(pos)
	pos_dict = creatDict(pos)
	print pos_dict
	pos_train = [[pos_dict[t] for t in sent] for sent in pos]
	
	d1_train = np.array([[d+maxl for d in sent] for sent in d1])
	d2_train = np.array([[d+maxl for d in sent] for sent in d2])
	y_train = np.zeros((len(sents), len(lables)))
	for i in range(y_train.shape[0]):
#			print y[i]
		y_train[i, y[i]] = 1

	return X_t, y_train, d1_train, d2_train, pos_train, pos_dict, maxl


def readData(fname):
	"""
	s1 : (int) entity one start place
	e1 : (int) entity one end place
	s2 : (int) entity two start place
	e2 : (int) entity two end place
	entity1 : (string) first entity in sentence
	entity2 : (string) sencond entity in sentence
	rel: (string) relation name ig. TrAP = (e1,e2), TrAP_r = (e2,e1)
	sent: sentence list
	"""
	with open(fname) as f:
		sent_list = []
		pos_list = []
		chunk_list = []
		short_dep_list = []
		entity1_list = []
		entity2_list = []
		entity1_s_e_list = []	#int list [s,e]
		entity2_s_e_list = [] 	#int list [s,e]	
		rel_list = []		
		for line in f:			 
			line = line.lower()
			sent,rel_part = line.strip().split("|||")[0:2]

			sent_l = sent.strip().split(' ')
			sent_list.append(sent_l)

			#pos tagging
#			pos_tmp = ann.getAnnotations(sent)['pos']
			pos_tmp = nltk.pos_tag(sent_l)
			if(len(pos_tmp) == len(sent_l)):
				pos_list.append(zip(*pos_tmp)[1])
			else:
				print "pos and sent lenth not matching"
				print pos_tmp
				print sent_l
				exit(0)

			#chunking
			chunk_tmp = ann.getAnnotations(sent)['chunk']
			if(len(chunk_tmp) == len(sent_l)):
				chunk_list.append(zip(*chunk_tmp)[1])
			else:								
				print "chunk and sen length not matching"				 
				print chunk_tmp
				print sent_l
				exit(0)
			
			
			tmp = rel_part.strip().split("||")
			e1 = tmp[0].partition('"')[-1].rpartition('"')[0]
			e1_s = int(tmp[0].strip().split()[-2].split(':')[1])
			e1_e = int(tmp[0].strip().split()[-1].split(':')[1])
			r = tmp[1].partition('"')[-1].rpartition('"')[0]
			e2 = tmp[2].partition('"')[-1].rpartition('"')[0]
			e2_s = int(tmp[2].strip().split()[-2].split(':')[1])
			e2_e = int(tmp[2].strip().split()[-1].split(':')[1])

			if ( e1_s < e2_s ) :
				entity1 = e1
				entity2 = e2
				entity1_s_e = [e1_s, e1_e] 
				enitty2_s_e = [e2_s, e2_e]
				rel = r
			else:		
				entity1 = e2
				entity2 = e1
				entity1_s_e = [e2_s, e2_e] 
				entity2_s_e = [e1_s, e1_e]
				rel = r	+ "_r"

			entity1_list.append(entity1)	 
			entity2_list.append(entity2)
			entity1_s_e_list.append(entity1_s_e)
			entity2_s_e_list.append(entity2_s_e)
			rel_list.append(rel)

			short_dep = shortDep(sent, entity1, entity2)
			short_dep_list.append(short_dep)

		f.close()
	return sent_list, pos_list, chunk_list, short_dep_list, entity1_list, entity2_list, entity1_s_e_list, entity2_s_e_list,		rel_list

