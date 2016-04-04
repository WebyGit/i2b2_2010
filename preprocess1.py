"""
655358166_WGH_32
Srom In Labor
(['labor', 2, 2, 'problem'], ['srom', 0, 0, 'problem'])
['srom', 'PIP', 'labor']
"""

ftrain = "data/combine.train"
fp = open(ftrain, 'r')
samples = fp.read().strip().split('\n\n\n')

sent_list = []
sent_length = []
sent_cont = []
sent_lable = []
for sample in samples:
	name, sent, entitis, relation = sample.strip().split('\n')	
	sent_length.append(len(sent.split()))
	sent_list.append(name)
	sent_cont.append(sent)
	sent_lable.append(relation)
print "number of sample", len(sent_list)

list_pair = zip(sent_length, sent_list, sent_cont, sent_lable)
list_pair.sort(reverse=True)
count = 0
for i in range(len(list_pair)):
#	print list_pair[i][0]
	if list_pair[i][0] < 50 :
		count += 1
print count


