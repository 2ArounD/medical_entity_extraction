export OUT_DIR="/output/"
export NER_DIR="/floyd/input/nerdata/NCBI-disease/"
export BIOBERT_DIR="/floyd/input/biobert/biobert_v1.1_pubmed/"
export NET="squeezeDet+BN"

floyd run \
--data 2around/datasets/pre_trained_weights/:biobert \
--data 2around/datasets/nerdata/:nerdata \
--env tensorflow-1.11 \
--gpu \
--max-runtime 1800 \
 "python3 ./train.py \
  --biobert_dir=$BIOBERT_DIR \
  --ner_dir=$NER_DIR \
  --output_dir=$OUT_DIR"

