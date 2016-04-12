import xml.etree.ElementTree as ET
import glob

#fileList1 = glob.glob("../DDI_SEMeVAL2013/DrugBank/*.xml")
#fileList2 = glob.glob("../DDI_SEMeVAL2013/MedLine/*.xml")

#fileList = fileList1 + fileList2

fileList = ['../DDI_SEMeVAL2013/DrugBank/Abarelix_ddi.xml']

cnt = 0
for fname in fileList:
  tree = ET.parse(fname)
  doc = tree.getroot()
  cnt += 1
  for sent in doc:
	text = sent.attrib['text']
#	print fname +" "+ sent.attrib['id']
#	print text.replace('\n', ' ').strip()
	entity_list = []
	interact_list = []

	for entity_pair in sent:		
		if(entity_pair.tag == 'entity'):
			eid = entity_pair.attrib['id'] 
			place = entity_pair.attrib['charOffset'] 
			etype = entity_pair.attrib['type'] 
			etext = entity_pair.attrib['text']
		#	print eid+"|"+place+"|"+etype+"|"+etext
			entity_list.append([eid, place, etype, etext])
		
		elif(entity_pair.tag == 'pair'):
			pid = entity_pair.attrib['id']
			ddi = entity_pair.attrib['ddi']
			if ddi == 'true':
				p_type = entity_pair.attrib['type']
			else:
				p_type = 'none'
			
			
			e1 = entity_pair.attrib['e1']
			e2 = entity_pair.attrib['e2']

			interact_list.append([pid, e1, ddi, p_type, e2])

	if len(interact_list) > 1:		
		for interact in interact_list:			
			for entity in entity_list:
 				if interact[1] == entity[0] :
					e1 = entity
				if interact[4] == entity[0]:
					e2 = entity
#			print e1[0]+"|"+e1[1]+"|"+e1[2]+"|"+e1[3]+"||"+interact[2]+"|"+interact[3]+"||"+e2[0]+"|"+e2[1]+"|"+e2[2]+"|"+e2[3]
			print text.replace('\n', ' ').strip()
			print e1[3]+'|'+e1[2]+"||"+interact[2]+"|"+interact[3]+"||"+e2[3]+"|"+e2[2]
			print '\n' 
