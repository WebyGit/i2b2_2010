from sklearn.cross_validation import KFold
import numpy as np
import sys

sys.path.append('../')
from utils import *
from cnn_train import *


#ftrain = "../i2b2_data/combine.train"
#ftrain = "../i2b2_data/temp.train"
ftrain = '../i2b2_data/beth.train'
#ftrain = '../i2b2_data/test.train'



sent_contents, entity1_list, entity2_list, sent_lables = readData(ftrain)

# Featurizer
pos_tag_list = makePosFeatures(sent_contents)
d1_list, d2_list, type_list = makeDistanceFeatures(sent_contents, entity1_list, entity2_list)

#padding
sent_contents,seq_len = makePaddedList(sent_contents)
pos_tag_list,_ = makePaddedList(pos_tag_list)
d1_list,_ = makePaddedList(d1_list)
d2_list,_ = makePaddedList(d2_list)
type_list,_ = makePaddedList(type_list)

# Wordlist
word_dict = makeWordList(sent_contents)
pos_dict = makeWordList(pos_tag_list)
d1_dict = makeWordList(d1_list)
#print "d1_dict", d1_dict
d2_dict = makeWordList(d2_list)
type_dict = makeWordList(type_list)

#label_dict = makeRelList(sent_lables)
#label_dict = {'other':0, 'TrWP': 1, 'TeCP': 2, 'TrCP': 3, 'TrNAP': 4, 'TrAP': 5, 'PIP': 6, 'TrIP': 7, 'TeRP': 8}
label_dict = {'other':0, 'TeCP': 1, 'TrCP': 2, 'TrAP': 3, 'PIP': 4, 'TeRP': 5}
print label_dict 

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

Y_t = mapLabelToId(sent_lables, label_dict)
Y_train = np.zeros((len(Y_t),label_dict_size))
for i in range(len(Y_t)):
	Y_train[i][Y_t[i]] = 1.0

"""
print W_train.shape
print P_train.shape 
print d1_train.shape
print d2_train.shape
print T_train.shape
print Y_train.shape
"""


fp = open("i2b2_results.txt",'w')

kf = KFold(len(W_train), n_folds=5)
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
			type_dict_size)		#type vocab length	
			

	y_true_list, y_pred_list = train.cnnTrain(W_tr, W_te, P_tr, P_te, d1_tr, d1_te, d2_tr, d2_te, T_tr, T_te, Y_tr, Y_te)

#	print "Precision", sk.metrics.precision_score(y_true, y_pred, average=None )
#	print "Recall", sk.metrics.recall_score(y_true, y_pred, average=None )
#	print "f1_score", sk.metrics.f1_score(y_true, y_pred, average=None )
#	print "confusion_matrix"
#	print sk.metrics.confusion_matrix(y_true, y_pred)
	
	for y_true, y_pred in zip(y_true_list, y_pred_list):
		fp.write(str(sk.metrics.precision_score(y_true, y_pred, average=None )))
		fp.write('\n')
		fp.write(str(sk.metrics.recall_score(y_true, y_pred, average=None )))
		fp.write('\n')
		fp.write(str(sk.metrics.f1_score(y_true, y_pred, average=None)))
		fp.write('\n')
		fp.write('\n')

	fp.write('\n')
	fp.write('\n')	
 



