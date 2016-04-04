from sklearn.feature_extraction import DictVectorizer
import numpy as np
from sklearn import svm

from helper import *

vec = DictVectorizer()
fname = "data/full_input.data"
#fname = "data/tmp.data"

#ll = makeLabelList(fname)
#print ll

sent_list, pos_list, chunk_list, short_dep_list, entity1_list, entity2_list, rel_list = readDataThroughGenia(fname)

word_dict =	makeWordList(sent_list)
pos_dict  = 	makeWordList(pos_list)
chunk_dict= 	makeWordList(chunk_list)
rel_dict  = 	makeRelList(rel_list)

print rel_dict

"""
for i in range(len(sent_list)):
	print"sent :", sent_list[i]
	print"pos  :", pos_list[i]
	print"chunk:", chunk_list[i]
	print"dep :", short_dep_list[i]
"""
 

"""
data = readData('data/tmp.data')
# sent_list.append([sent, r, e1, e1_s, e1_e, e2, e2_s, e2_e])
features = []
for i in range(len(data)):
	sent_feat= {}
	sent = data[i][0]
	sent = ['<s>'] + sent +['</s>']
#	print sent
	sent_feat['e1'] = data[i][2]
	sent_feat['e2'] = data[i][5]	
#	print data[i][3]
 
	sent_feat['l1e1']= sent[int(data[i][3])-2]
	sent_feat['l1e2']= sent[int(data[i][6])-2]
	sent_feat['r1e1']= sent[int(data[i][3])]
	sent_feat['r1e1']= sent[int(data[i][6])]
	
	features.append(sent_feat)
#	print sent

label = {'trap':0, 'pip':1, 'terp':2, 'trip':3, 'trwp':4, 'trcp':5, 'trnap':6, 'tecp':7 }
#print features
X_train = vec.fit_transform(features).toarray()
print vec.get_feature_names()
Y_train = [label[data[i][1]] for i in range(len(data))]
#print Y_train

clf = svm.SVC()

clf.fit(X_train, Y_train)

print "predict",clf.predict(X_train[2])

"""



