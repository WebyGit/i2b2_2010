EU-ADR Corpus Charactersitics
--------------------------------------------------------------------------------

The EU-ADR corpus is distributed within three files:

- EUADR_drug_disease.csv: describes relations between drugs and diseases.
- EUADR_drug_target.csv: describes relations between drugs and targets.
- EUADR_target_disease.csv: describes relations between targets and diseases.

The format of the three files are as follows with header and tab delimiters:

Column  1: Associarion type (PA, NA, SA or FA).
Column  2: Number of PubMedID .
Column  3: Number of sentence in the abstract.
Column  4: Text of entity1 in the sentence.
Column  5: Begin offset of entity1 at 'sentence level'
Column  6: End offset of entity1 at 'sentence level'
Column  7: Entity1 type.
Column  8: Text of entity1 in the sentence.
Column  9: Begin offset of entity1 at 'sentence level'.
Column 10: End offset of entity1 at 'sentence level'.
Column 11: Entity1 type.
Column 12: Sentence.

--------------------------------------------------------------------------------

If you use this corpus for any publication purposes, you are requested to cite the source article:

van Mulligen EM, Fourrier-Reglat A, Gurwitz D, Molokhia M, Nieto A, Trifiro G, Kors JA, Furlong LI, "The EU-ADR corpus: annotated drugs, diseases, targets, and their relationships." J Biomed Inform 2012, 45:879–884 doi:10.1016/j.jbi.2012.04.004.

van Mulligen EM1, Fourrier-Reglat A, Gurwitz D, Molokhia M, Nieto A, Trifiro G, Kors JA, Furlong LI, "The EU-ADR corpus is made available under the Open Database License whose full text can be found at http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License whose text can be found at http://opendatacommons.org/licenses/odbl/1.0/

--------------------------------------------statistics-----------------------------------

sunilitggu@ubuntu:~/Downloads/EUADR_Corpus_IBIgroup$ cat *.csv> combine.txt
sunilitggu@ubuntu:~/Downloads/EUADR_Corpus_IBIgroup$ grep 'PA' combine.txt |wc
    533   23719  165709
sunilitggu@ubuntu:~/Downloads/EUADR_Corpus_IBIgroup$ grep 'FA' combine.txt |wc
    233   10692   75546
sunilitggu@ubuntu:~/Downloads/EUADR_Corpus_IBIgroup$ grep 'NA' combine.txt |wc
     86    4958   35183
sunilitggu@ubuntu:~/Downloads/EUADR_Corpus_IBIgroup$ grep 'SA' combine.txt |wc
     70    3037   20602
sunilitggu@ubuntu:~/Downloads/EUADR_Corpus_IBIgroup$ wc combine.txt 
   849  37659 263713 combine.txt




#############################################Results################################

[ 0.          0.68627451][ 0.  1.][ 0.          0.81395349]
[ 0.79487179  0.85087719][ 0.64583333  0.92380952][ 0.71264368  0.88584475]
[ 0.91836735  0.97115385][ 0.9375      0.96190476][ 0.92783505  0.96650718]
[ 0.93181818  0.93577982][ 0.85416667  0.97142857][ 0.89130435  0.95327103]
[ 0.86538462  0.97029703][ 0.9375      0.93333333][ 0.9         0.95145631]


[ 0.          0.75163399][ 0.  1.][ 0.          0.85820896]
[ 0.65714286  0.87288136][ 0.60526316  0.89565217][ 0.63013699  0.88412017]
[ 0.96428571  0.912     ][ 0.71052632  0.99130435][ 0.81818182  0.95      ]
[ 0.7254902   0.99019608][ 0.97368421  0.87826087][ 0.83146067  0.93087558]
[ 0.89655172  0.90322581][ 0.68421053  0.97391304][ 0.7761194   0.93723849]


[ 0.34640523  0.        ][ 1.  0.][ 0.51456311  0.        ]
[ 1.          0.66225166][ 0.03773585  1.        ][ 0.07272727  0.79681275]
[ 0.91071429  0.97938144][ 0.96226415  0.95      ][ 0.93577982  0.96446701]
[ 1.          0.90909091][ 0.81132075  1.        ][ 0.89583333  0.95238095]
[ 0.86885246  1.        ][ 1.    0.92][ 0.92982456  0.95833333]


[ 0.          0.67105263][ 0.  1.][ 0.          0.80314961]
[ 0.76470588  0.79661017][ 0.52        0.92156863][ 0.61904762  0.85454545]
[ 0.86046512  0.88073394][ 0.74        0.94117647][ 0.79569892  0.90995261]
[ 0.8627451   0.94059406][ 0.88        0.93137255][ 0.87128713  0.93596059]
[ 0.92682927  0.89189189][ 0.76        0.97058824][ 0.83516484  0.92957746]


[ 0.          0.72368421][ 0.  1.][ 0.          0.83969466]
[ 0.61764706  0.8220339 ][ 0.5         0.88181818][ 0.55263158  0.85087719]
[ 0.90697674  0.97247706][ 0.92857143  0.96363636][ 0.91764706  0.96803653]
[ 0.86486486  0.91304348][ 0.76190476  0.95454545][ 0.81012658  0.93333333]
[ 0.7826087   0.94339623][ 0.85714286  0.90909091][ 0.81818182  0.92592593]


