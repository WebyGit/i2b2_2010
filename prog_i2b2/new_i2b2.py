from sklearn.cross_validation import KFold
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import networkx as nx
import numpy as np
import sys
import re
import pickle

from practnlptools.tools import Annotator
ann=Annotator()

sys.path.append('../')
from utils1 import *
from cnn_train import *

#define
N = 1000 			# number epoch
M = 500				
batch_size = 50
num_filter = 70
filter_size = [2,3,5]
pos_feature = True
chunk_feature = True
type_feature = True
distance_feature = True
vector = 'rand'			# "wv" for wordvector and "rand" for random vector


ftrain = "../i2b2_data/combine.train"
#ftrain = "../i2b2_data/temp.train"
#ftrain = '../i2b2_data/beth.train'
#ftrain = '../i2b2_data/test.train'
fwv = '../word2vec/script/i2b2_corpus_word2vec.txt'

print "File reading"
sent_contents, entity1_list, entity2_list, sent_lables = readData(ftrain)
print 'Making Features'
sent_list, pos_tag_list, chunk_tag_list, d1_list, d2_list, type_list, dep_parse_list = makeFeatures(sent_contents, entity1_list, entity2_list, sent_lables)

print "padding"
sent_list = makePaddedListSent(sent_list)

pos_tag_list = makePaddedList(pos_tag_list)
chunk_tag_list = makePaddedList(chunk_tag_list)
d1_list = makePaddedList(d1_list)
d2_list = makePaddedList(d2_list)
type_list = makePaddedList(type_list)
dep_parse_list = makePaddedList(dep_parse_list)

# Wordlist
word_dict = makeWordList(sent_list)
pos_dict = makeWordList(pos_tag_list)
chunk_dict = makeWordList(chunk_tag_list)
d1_dict = makeWordList(d1_list)
d2_dict = makeWordList(d2_list)
type_dict = makeWordList(type_list)
dep_parse_dict = makeWordList(dep_parse_list)

#label_dict = {'other':0, 'TrWP': 1, 'TeCP': 2, 'TrCP': 3, 'TrNAP': 4, 'TrAP': 5, 'PIP': 6, 'TrIP': 7, 'TeRP': 8}
label_dict = {'other':0, 'TeCP': 1, 'TrCP': 2, 'TrAP': 3, 'PIP': 4, 'TeRP': 5}

#vocabulary size
word_dict_size = len(word_dict)
pos_dict_size = len(pos_dict)
chunk_dict_size = len(chunk_dict)
d1_dict_size = len(d1_dict)
d2_dict_size = len(d2_dict)
type_dict_size = len(type_dict)
dep_dict_size = len(dep_parse_dict)
label_dict_size = len(label_dict)

# Mapping
W_train =  np.array(mapWordToId(sent_list, word_dict))
P_train = np.array(mapWordToId(pos_tag_list, pos_dict))
C_train = np.array(mapWordToId(chunk_tag_list, chunk_dict))
d1_train = np.array(mapWordToId(d1_list, d1_dict))
d2_train = np.array(mapWordToId(d2_list, d2_dict))
T_train = np.array(mapWordToId(type_list,type_dict))
D_train = np.array(mapWordToId(dep_parse_list, dep_parse_dict))

 
Y_t = mapLabelToId(sent_lables, label_dict)
Y_train = np.zeros( (len(Y_t), len(label_dict) ) )
for i in range(len(Y_t)):
	Y_train[i][Y_t[i]] = 1.0



with open('filename.pickle', 'wb') as handle:
	pickle.dump(W_train, handle)
	pickle.dump(P_train, handle)
	pickle.dump(C_train, handle)
	pickle.dump(d1_train, handle)
	pickle.dump(d2_train, handle)
	pickle.dump(T_train, handle)
	pickle.dump(D_train, handle)
	pickle.dump(Y_train, handle)
	pickle.dump(word_dict, handle)
	pickle.dump(pos_dict, handle)
	pickle.dump(chunk_dict, handle)
	pickle.dump(d1_dict, handle)
	pickle.dump(d2_dict, handle)
	pickle.dump(type_dict, handle)
	pickle.dump(dep_parse_dict, handle)
	pickle.dump(label_dict, handle)


"""
with open('filename.pickle', 'rb') as handle:
	W_train = pickle.load(handle)
	P_train = pickle.load(handle)
	C_train = pickle.load(handle)
	d1_train = pickle.load(handle)
	d2_train = pickle.load(handle)
	T_train = pickle.load(handle)
	D_train = pickle.load(handle)
	Y_train = pickle.load(handle)
	word_dict= pickle.load(handle)
	pos_dict = pickle.load(handle)
	chunk_dict = pickle.load(handle)
	d1_dict = pickle.load(handle)
	d2_dict = pickle.load(handle)
	type_dict = pickle.load(handle)
	dep_parse_dict = pickle.load(handle)
	label_dict = pickle.load(handle)
"""

fp = open("i2b2_results.txt",'w')
seq_len = max([len(sent) for sent in W_train])

kf = KFold(len(W_train), n_folds=5)
acc_list = []
for train, test in kf:
	W_tr, W_te = W_train[train], W_train[test]
	P_tr, P_te = P_train[train], P_train[test]
	C_tr, C_te = C_train[train], C_train[test]
	D_tr, D_te = D_train[train], D_train[test]
	d1_tr, d1_te = d1_train[train], d1_train[test]
	d2_tr, d2_te = d2_train[train], d2_train[test]
	T_tr, T_te = T_train[train], T_train[test]
	Y_tr, Y_te = Y_train[train], Y_train[test]
#	print "seq_len", seq_len
	cnn = CNN_Relation(label_dict_size, seq_len, word_dict_size, pos_dict_size, chunk_dict_size, dep_dict_size, d1_dict_size, d2_dict_size, type_dict_size)			

 	time = range(len(W_tr))
	step = np.random.shuffle(time)
	j = 0
	
	y_true_list = []
	y_pred_list = []
	for i in range(N):
		cnn.train_step(W_tr, P_tr, C_tr, d1_tr, d2_tr, T_tr, D_tr, Y_tr)
		"""
		if(j >= len(W_tr) - batch_size):
			j=0
			s = range(j, j+batch_size)
			cnn.train_step(W_tr[s], P_tr[s], C_tr[s], d1_tr[s], d2_tr[s], T_tr[s], D_tr[s], Y_tr[s])
			j += batch_size
		"""		
		if (i%M) == 0:
			acc, pred = cnn.test_step(W_te, P_te, C_te, d1_te, d2_te, T_te, D_te, Y_te)
			y_true = np.argmax(Y_te, 1)
			y_pred = pred	
			y_true_list.append(y_true)
			y_pred_list.append(y_pred)
	
	for y_true, y_pred in zip(y_true_list, y_pred_list):
		fp.write(str(precision_score(y_true, y_pred, average=None )))
		fp.write('\n')
		fp.write(str(recall_score(y_true, y_pred, average=None )))
		fp.write('\n')
		fp.write(str(f1_score(y_true, y_pred, average=None)))
		fp.write('\n')
		fp.write('\n')

	fp.write('\n')
	fp.write('\n')	
 

