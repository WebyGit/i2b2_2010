#He was noted to have an erythematous perianal rash and for this was started on Nystatin powder . ||| c="nystatin powder" 64:15 64:16||r="TrAP"||c="an erythematous perianal rash" 64:5 64:8 ||| record-107.txt

#TrAP = (e1, e2)
#TrAP_ = (e2, e1)

from helper import *
from cnn_text import CNN_Relation

import numpy as np
import tensorflow as tf
import random


#define
w_emb_size = 20
p1_emb_size = 5
p2_emb_size = 5
pos_emb_size = 5

emb_size = w_emb_size + p1_emb_size + p2_emb_size + pos_emb_size
num_filters = 20
filter_sizes = [3,4,5]
dropout_keep_prob = 0.5
l2_reg_lambda=0.0
ftrain = "data/full_input.data"
fwl = "data/word.list"

lables = {'trip':0, 'trip_':1, 'trwp':2, 'trwp_':3, 'trcp':4, 'trcp_':5, 'trap':6, 'trap_':7, 'trnap':8, 'trnap_':9, 'terp':10, 'terp_':11, 'tecp':12, 'tecp_':13, 'pip':14, 'pip_':15}

num_classes = len(lables)

sents =  readData(ftrain)
wordlist = readWordList(fwl)
X_train, y_train, p1_train, p2_train, pos_train, pos_dict, seq_len = wordPosMapping(sents, wordlist, lables)
vocab_size = len(wordlist)

cnn = CNN_Relation(
		seq_len = seq_len, 
		num_classes = num_classes, 
		vocab_size = vocab_size, 
		w_emb_size = w_emb_size, 
		p1_emb_size = p1_emb_size, 
		p2_emb_size = p2_emb_size, 
		pos_emb_size = pos_emb_size,
		pos_dict = pos_dict,
		filter_sizes = filter_sizes, 
		num_filters = num_filters, 
		l2_reg_lambda = 0.0 
	)


sess = tf.Session()

optimizer = tf.train.AdamOptimizer(1e-2)

grads_and_vars = optimizer.compute_gradients(cnn.loss)
global_step = tf.Variable(0, name="global_step", trainable=False)
train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

sess.run(tf.initialize_all_variables())

#a1, a2 = sess.run([X, X_expanded], {x:X_train, x1:p1_train, x2:p2_train})
#accuracy, loss = sess.run([h, pooled], {x:X_train, x1:p1_train, x2:p2_train, input_y:y_train})

def train_step(x_batch, x1_batch, x2_batch, x3_batch, y_batch):
	feed_dict = {
		cnn.x :x_batch,
		cnn.x1:x1_batch, 
		cnn.x2:x2_batch,
		cnn.x3:x3_batch,
		cnn.input_y:y_batch,
		cnn.dropout_keep_prob: 0.5
	}
 	_, step, loss, accuracy = sess.run([train_op, global_step, cnn.loss, cnn.accuracy], feed_dict)
 	print ("step "+str(step) + " loss "+str(loss) +" accuracy "+str(accuracy))


def test_step(x_batch, x1_batch, x2_batch, x3_batch, y_batch):
	feed_dict = {
		cnn.x :x_batch,
		cnn.x1:x1_batch, 
		cnn.x2:x2_batch,
		cnn.x3:x3_batch,
		cnn.input_y:y_batch,
		cnn.dropout_keep_prob:1.0
	}
 	_, step, loss, accuracy = sess.run([train_op, global_step, cnn.loss, cnn.accuracy], feed_dict)
	print "Accuracy in test data", accuracy


tot = len(X_train)
a = range(tot)
random.shuffle(a)
 
for i in range(100):
	train_step(X_train[0:2000], p1_train[0:2000], p2_train[0:2000], pos_train[0:2000], y_train[0:2000])
	train_step(X_train[2000:4000], p1_train[2000:4000], p2_train[2000:4000], pos_train[2000:4000], y_train[2000:4000])
	train_step(X_train[4000:6000], p1_train[4000:6000], p2_train[4000:6000], pos_train[4000:6000], y_train[4000:6000])
	train_step(X_train[6000:8000], p1_train[6000:8000], p2_train[6000:8000], pos_train[6000:8000], y_train[6000:8000])

test_step(X_train[8000:-1], p1_train[8000:-1], p2_train[8000:-1], pos_train[8000:-1], y_train[8000:-1])









