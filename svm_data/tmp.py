import sys

#sys.path.append('../')
fname = "../data/beth.train"

fp = open(fname, 'r')

for line in fp.read().split('\n'):
	print line

