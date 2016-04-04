DATA_DIR=../data
BIN_DIR=../bin
SRC_DIR=../src
TEXT_DATA=/home/sunilitggu/Desktop/i2b2_relation

VECTOR_DATA=$DATA_DIR/cbow_50d_w9.bin

pushd ${SRC_DIR} && make; popd

if [ ! -e $VECTOR_DATA ]; then
 
  echo -----------------------------------------------------------------------------------------------------
  echo -- Training vectors...
  time $BIN_DIR/word2vec -train $TEXT_DATA -output $VECTOR_DATA -cbow 1 -size 50 -window 9 -negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 1
  
fi

echo -----------------------------------------------------------------------------------------------------
echo -- distance...

$BIN_DIR/distance $DATA_DIR/$VECTOR_DATA
