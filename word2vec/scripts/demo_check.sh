DATA_DIR=../data
BIN_DIR=../bin
SRC_DIR=../src

TEXT_DATA=/home/muneeb/Complete_Pubmed_Corpus/Extracted_corpus/pubmed.txt
VECTOR_DATA=$DATA_DIR/wordVector500.bin

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA
