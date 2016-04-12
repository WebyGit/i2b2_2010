from sklearn.cross_validation import KFold
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import sys
import pickle
sys.path.append('../')
from utils import *
from cnn_train import *

#ftrain = "tmp"
ftrain = 'processed_ddi.txt'

sent_list, e1_list, e2_list, rel_list = readData(ftrain)
 
sent_list, pos_list, chunk_list, d1_list, d2_list, type_list, lable_list = makeFeatures(sent_list, e1_list, e2_list, rel_list)

print "padding"
sent_list = makePaddedList(sent_list)
pos_tag_list = makePaddedList(pos_list)
chunk_tag_list = makePaddedList(chunk_list)
d1_list = makePaddedList(d1_list)
d2_list = makePaddedList(d2_list)
type_list = makePaddedList(type_list)


# Wordlist
word_dict = makeWordList(sent_list)
pos_dict = makeWordList(pos_tag_list)
chunk_dict = makeWordList(chunk_tag_list)
d1_dict = makeWordList(d1_list)
d2_dict = makeWordList(d2_list)
type_dict = makeWordList(type_list)

label_dict = makeLableList(lable_list)

#vocabulary size
word_dict_size = len(word_dict)
pos_dict_size = len(pos_dict)
chunk_dict_size = len(chunk_dict)
d1_dict_size = len(d1_dict)
d2_dict_size = len(d2_dict)
type_dict_size = len(type_dict)
label_dict_size = len(label_dict)

# Mapping
W_train =  np.array(mapWordToId(sent_list, word_dict))
P_train = np.array(mapWordToId(pos_tag_list, pos_dict))
C_train = np.array(mapWordToId(chunk_tag_list, chunk_dict))
d1_train = np.array(mapWordToId(d1_list, d1_dict))
d2_train = np.array(mapWordToId(d2_list, d2_dict))
T_train = np.array(mapWordToId(type_list,type_dict))

 
Y_t = mapLabelToId(lable_list, label_dict)
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
	pickle.dump(Y_train, handle)
	pickle.dump(word_dict, handle)
	pickle.dump(pos_dict, handle)
	pickle.dump(chunk_dict, handle)
	pickle.dump(d1_dict, handle)
	pickle.dump(d2_dict, handle)
	pickle.dump(type_dict, handle)	 
	pickle.dump(label_dict, handle) 
 
