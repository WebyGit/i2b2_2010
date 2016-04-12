import csv
import nltk
from nltk.tokenize import WordPunctTokenizer
tokenizer = WordPunctTokenizer()
from sklearn.cross_validation import KFold
import numpy as np
import sklearn as sk


#from utils import *
from cnn_train import *

#fname = "drug_disease_target/EUADR_Corpus_IBIgroup/EUADR_drug_disease.csv"
fname = "drug_disease_target/EUADR_Corpus_IBIgroup/combine.txt"
batch_size = 50



def dataRead(fname):
    with open(fname, 'rb') as data:
	reader = csv.reader(data, delimiter='\t')
	sent_list = []
	e1_e2_list = []
	e1_e2_type_list = []
	e1_e2_start_list = []
	e1_e2_end_list = []
	lable_list = []
	header = True
	for row in reader:
#		print row
		if header :
			header = False
			continue
		asso_type, pm_id, sent_id, e1, e1_s, e1_e, e1_type, e2, e2_s, e2_e, e2_type, sent = row
#		if(asso_type == 'NA' or asso_type == 'SA'):
#			continue
		sent_list.append(sent)
		if(int(e1_s) < int(e2_s)):
			e1_e2_list.append([e1, e2])
			e1_e2_type_list.append([e1_type, e2_type])
			e1_e2_start_list.append([e1_s, e2_s])
			e1_e2_end_list.append([e1_e, e2_e])
#			print 'AAA'
		else:
			e1_e2_list.append([e2, e1])
			e1_e2_type_list.append([e2_type, e1_type])
			e1_e2_start_list.append([e2_s, e1_s])
			e1_e2_end_list.append([e2_e, e1_e])
#			print "BBB"
		lable_list.append(asso_type)
    return sent_list, e1_e2_list, e1_e2_type_list, e1_e2_start_list, e1_e2_end_list, lable_list

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
#	wl['unkown'] = 0	
	for w,f in wf.iteritems():		
		wl[w] = i
		i += 1
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

def makeFeature(sent_list, entity_list, entity_type_list):
    sent_l = []
    d1_list = []
    d2_list = []
    type_list = []
    for sent, entity_l, entity_type in zip(sent_list, entity_list, entity_type_list):
	sent = sent.replace(').', ') .')
#	sent_list = nltk.word_tokenize(sent)
	sent_list = tokenizer.tokenize(sent)
#	print sent_list
#	print entity_l
	sent_l.append(sent_list)
	maxl = len(sent_list)
#	entity1 = nltk.word_tokenize(entity_l[0])
#	entity2 = nltk.word_tokenize(entity_l[1])
	entity1 = tokenizer.tokenize(entity_l[0])
	entity2 = tokenizer.tokenize(entity_l[1])
	s1 = sent_list.index(entity1[0])
	e1 = sent_list.index(entity1[-1])
	s2 = sent_list.index(entity2[0])
	e2 = sent_list.index(entity2[-1])
	
#	print e1, e2
#	print s1,s2
	
#	print sent_l
	d1 = []
	for i in range(maxl):
		if i < s1 :
			d1.append(str(i - s1))
		elif i > e1 :
			d1.append(str(i - e1 ))
		else:
			d1.append('0')
	d1_list.append(d1)

	d2 = []
	for i in range(maxl):
		if i < s2 :
			d2.append(str(i - s2))
		elif i > s2 :
			d2.append(str(i - s2))
		else:
			d2.append('0')		
	d2_list.append(d2)
	
	t = []
	for i in range(maxl):
		t.append('Out')
	for i in range(s1,e1+1):
		t[i] = entity_type[0]
		
	for i in range(s2, e2+1):
		t[i] = entity_type[1]
 	type_list.append(t) 	

    return sent_l, d1_list, d2_list, type_list

def makePosFeatures(sent_contents):
	pos_tag_list = []
	for sent in sent_contents:
#		tags = tagger.parse(sent)
#		sent_t, sent_o, sent_pos, sent_chunk, sent_bio = zip(*tags)
		pos_tag = nltk.pos_tag(sent)
		pos_tag = zip(*pos_tag)[1]
#		print pos_tag
		pos_tag_list.append(pos_tag)		
	return pos_tag_list 

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

	return T, maxl

def mapLabelToId(sent_lables, label_dict):
	return [label_dict[label] for label in sent_lables]

def mapWordToId(sent_contents, word_dict):
	T = []
	for sent in sent_contents:
		t = []
		for w in sent:
			t.append(word_dict[w])
		T.append(t)
	return T


sent_list,entity_list,entity_type_list,_,_,label_list = dataRead(fname)
sent_contents, d1_list, d2_list, type_list = makeFeature(sent_list, entity_list, entity_type_list)
pos_tag_list = makePosFeatures(sent_contents)
 

#padding
sent_contents,seq_len = makePaddedList(sent_contents)
pos_tag_list,_ = makePaddedList(pos_tag_list)
 
d1_list,_ = makePaddedList(d1_list)
d2_list,_ = makePaddedList(d2_list)
type_list,_ = makePaddedList(type_list)

# Wordlist
label_dict =  {'FA': 0, 'SA': 1, 'PA': 2, 'NA': 3}
#label_dict =  {'FA': 0, 'PA': 1}
print label_dict

word_dict = makeWordList(sent_contents)
d1_dict = makeWordList(d1_list)
d2_dict = makeWordList(d2_list)
type_dict = makeWordList(type_list)
pos_dict = makeWordList(pos_tag_list)

#vocabulary size
word_dict_size = len(word_dict)
pos_dict_size = len(pos_dict)
d1_dict_size = len(d1_dict)
d2_dict_size = len(d2_dict)
type_dict_size = len(type_dict)
label_dict_size = len(label_dict)

#print "pos dict", pos_dict
# Mapping
W_train =  np.array(mapWordToId(sent_contents, word_dict))
P_train = np.array(mapWordToId(pos_tag_list, pos_dict))
d1_train = np.array(mapWordToId(d1_list, d1_dict))
d2_train = np.array(mapWordToId(d2_list, d2_dict))
T_train = np.array(mapWordToId(type_list,type_dict))

Y_t = mapLabelToId(label_list, label_dict)
Y_train = np.zeros((len(Y_t),label_dict_size))
for i in range(len(Y_t)):
	Y_train[i][Y_t[i]] = 1.0


num_sample = len(Y_train)

print "seq length", seq_len

"""
print W_train.shape
print P_train.shape 
print d1_train.shape
print d2_train.shape
print T_train.shape
print Y_train.shape
"""
"""
#Shuffling
series = range(len(W_train))

series = random.shuffle(series)
W_train = W_train[[series]]
P_train = P_train[[series]]
d1_train = d1_train[[series]]
d2_train = d2_train[[series]]
T_train = T_train[[series]]
Y_train = Y_train[[series]]

print "len of samples", len(W_train)
"""
fp = open("reslt1.txt",'w')

kf = KFold(num_sample, n_folds=5)
acc_list = []
for train, test in kf:
	W_tr, W_te = W_train[train], W_train[test]
	P_tr, P_te = P_train[train], P_train[test]
	d1_tr, d1_te = d1_train[train], d1_train[test]
	d2_tr, d2_te = d2_train[train], d2_train[test]
	T_tr, T_te = T_train[train], T_train[test]
	Y_tr, Y_te = Y_train[train], Y_train[test]

	"""	
	print W_tr.shape, W_te.shape
	print P_tr.shape, P_te.shape 
	print d1_tr.shape, d1_te.shape
	print d2_tr.shape, d2_te.shape
	print T_tr.shape, T_te.shape
	print Y_tr.shape, Y_te.shape
	"""

	train = CNN_Train(label_dict_size,
			seq_len, 		#length of largest sent
			label_dict_size, 	#number of classes
			word_dict_size,		#word vocab length
			pos_dict_size,		#pos vocab length
			d1_dict_size,		#d1 vocab length
			d2_dict_size,		#d2 vocab length
			type_dict_size,		#type vocab length	
			batch_size)

	y_true_list, y_pred_list = train.cnnTrain(W_tr, W_te, P_tr, P_te, d1_tr, d1_te, d2_tr, d2_te, T_tr, T_te, Y_tr, Y_te)

#	print "Precision", sk.metrics.precision_score(y_true, y_pred, average=None )
#	print "Recall", sk.metrics.recall_score(y_true, y_pred, average=None )
#	print "f1_score", sk.metrics.f1_score(y_true, y_pred, average=None )
#	print "confusion_matrix"
#	print sk.metrics.confusion_matrix(y_true, y_pred)
	for y_true, y_pred in zip(y_true_list, y_pred_list):
		fp.write(str(sk.metrics.precision_score(y_true, y_pred, average=None )))
		fp.write(str(sk.metrics.recall_score(y_true, y_pred, average=None )))
		fp.write(str(sk.metrics.f1_score(y_true, y_pred, average=None)))
		fp.write('\n')
	fp.write('\n')
	fp.write('\n')	
 


















		
