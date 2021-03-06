from utils import *

import numpy as np
from sklearn import cross_validation
from sklearn.cross_validation import KFold
from sklearn.feature_extraction import DictVectorizer
from sklearn import datasets
from sklearn import svm
import re
import networkx as nx

#from geniatagger import GeniaTagger
#tagger = GeniaTagger('/home/sunilitggu/python_pack/geniatagger-3.0.2/geniatagger')
#from practnlptools.tools import Annotator
#ann=Annotator()


def makeFeatures(sent_contents):
	sent_list = []
	norm_sent_list = []
	pos_list = []
	chunk_list = []
	for sent in sent_contents:
		sent = ' '.join(sent)
		tags = tagger.parse(sent)
		sent_t, sent_o, sent_pos, sent_chunk, sent_bio = zip(*tags)
		sent_list.append(sent_t)
		norm_sent_list.append(sent_o)
		pos_list.append(sent_pos)
		chunk_list.append(sent_chunk)
	return sent_list, norm_sent_list, pos_list,chunk_list		

def readFeatures(fname):
#	with open(fname) as f:
	fp = open(fname, 'r')
	data = fp.read().strip().split('\n\n')

	sent_list = []
	norm_sent_list = []
	pos_list = []
	chunk_list = []

	for sent in data:
#		print sent
		if(len(sent.strip().split('\n')) == 4):
			s,n,p,c = sent.strip().split('\n')
			sent_list.append(s.strip().split())
			norm_sent_list.append(s.strip().split())
			pos_list.append(p.strip().split())
			chunk_list.append(c.strip().split())
	return sent_list, norm_sent_list, pos_list, chunk_list

def makeVector(sent_list, entity1_list, entity2_list, sent_lables, norm_sent, pos_list, chunk_list):

   features = []
   for i in range(len(sent_list)):
	sent_feat= {}
	sent = sent_list[i]

	sent = ['<s>'] + sent +['</s>']

#	print sent
	sent_feat['e1'] = entity1_list[i][0]
	sent_feat['e2'] = entity2_list[i][0]
 
 
	sent_feat['l1e1']= sent[entity1_list[i][1] - 1]
	sent_feat['l1e2']= sent[entity2_list[i][1] - 1]
	sent_feat['r1e1']= sent[entity1_list[i][2] + 1]
	sent_feat['r1e1']= sent[entity1_list[i][2] + 1]
		
	sent_feat['pos'] = '-'.join(pos_list[i])
	sent_feat['chunk'] = '-'.join(chunk_list[i])

	features.append(sent_feat)
 
   return features		
 


ftrain = "data/combine.train"
#ftrain = "data/temp.train"
#ftrain = 'data/beth.train'
#ftrain = 'data/test.train'
#label_dict = makeRelList(sent_lables)

label_dict = {'other':0, 'TrWP': 1, 'TeCP': 2, 'TrCP': 3, 'TrNAP': 4, 'TrAP': 5, 'PIP': 6, 'TrIP': 7, 'TeRP': 8}

sent_contents, entity1_list, entity2_list, sent_lables = readData(ftrain)

#sent_list, norm_sent_list, pos_list, chunk_list = makeFeatures(sent_contents)

sent_list, norm_sent_list, pos_list, chunk_list = readFeatures('svm_data/xae')

features_dict = makeVector(sent_list, entity1_list, entity2_list, sent_lables, norm_sent_list, pos_list, chunk_list)

vec = DictVectorizer()
X_train = vec.fit_transform(features_dict).toarray()
#print vec.get_feature_names()

#print X_train
Y_train = [label_dict[i] for i in sent_lables]


kf = KFold(len(X_train), n_folds=5)

acc_list = []
for train, test in kf:
	X_tr, X_te = X_train[train], X_train[test]
	Y_train = np.array(Y_train)
	Y_tr, Y_te = Y_train[train], Y_train[test]

	clf = svm.SVC(kernel='linear', C=1).fit(X_tr, Y_tr)
	a = clf.score(X_te, Y_te)

#	print y_test
	print "accuracy", a
	acc_list.append(a)

print "avg",np.mean(acc_list)


clf = svm.SVC()

clf.fit(X_train, Y_train)

print "predict",clf.predict(X_train[2])





"""
fp = open('svm_data/temp.train','w')

for sent,norm_sent,pos,chunk in zip(sent_list, norm_sent_list, pos_list, chunk_list):
	fp.write(' '.join(sent))
	fp.write('\n')
	fp.write(' '.join(norm_sent))
	fp.write('\n')
	fp.write(' '.join(pos))
	fp.write('\n')
	fp.write(' '.join(chunk))
	fp.write('\n')
	fp.write('\n')

"""



"""
iris = datasets.load_iris()
print iris.data.shape, iris.target.shape

X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)

print len(X_train), len(X_test)


clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)

a = clf.score(X_test, y_test)
print y_test
print "accuracy", a
"""



"""
kf = KFold(iris.data.shape[0], n_folds=10)
acc_list = []
for train, test in kf:
	X_train, X_test = iris.data[train], iris.data[test]
	y_train, y_test = iris.target[train], iris.target[test]
	print len(X_train), len(X_test)
	clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
	a = clf.score(X_test, y_test)
#	print y_test
	print "accuracy", a
	acc_list.append(a)

print "avg",np.mean(acc_list)

"""




