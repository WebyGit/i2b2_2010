import numpy as np
import re


def readData(fname):
	with open(fname) as f:
		sent_list = []		
		for line in f:			 
			line = line.lower()
			line = re.sub('\d','dg',line)
			sent,rel = line.strip().split("|||")[0:2]			 
			sent = sent.strip().split(' ')			 
			sent_list.append(sent)
		f.close()
	return sent_list

def readWordVector(fname):
	with open(fname) as f:
		wv = []
		wl = {}
		wl['unkown'] = 0
		i = 1
		
		for line in f:
			if len(line) < 50 :
				continue
			else:
				w = line.strip().split()[0]
				v = line.strip().split()[1:]
				v = map(float, v)
				wv.append(v)
				wl[w] = i
				i += 1
				
	wv = np.asarray(wv, dtype='float64')
	return wl,wv			


ifile = "/home/sunilitggu/Desktop/i2b2_relation/data/full_input.data"
wvfile = "/home/sunilitggu/Desktop/i2b2_relation/word2vec/scripts/i2b2_corpus_word2vec.txt"

sent_lists = readData(ifile)

#print "length sentlist", len(sent_lists)

wl,wv = readWordVector(wvfile)

#print "len wl", len(wl)

X_train = []
cnt = 0
ucnt = 0
for sent in sent_lists:
	x = []
	for w in sent:
		if w in wl:
			x.append(wl[w])
		else:
			x.append(wl['unkown'])
			ucnt += 1
			print w
		cnt += 1
	X_train.append(x)

#print "X_train", len(X_train)

#print "ucnt", ucnt
#print "cnt", cnt


