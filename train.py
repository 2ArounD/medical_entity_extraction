import os
import argparse
import pdb


parser = argparse.ArgumentParser()
parser.add_argument('--biobert_dir', dest='biobert_dir' , type=str,
                    default='../data/pre_training/biobert_v1.1_pubmed/',
                    help='directory with biobert pretrained weights, config and vocab')

parser.add_argument('--ner_dir', dest='ner_dir' , type=str,
                    default='../data/NERdata/NCBI-disease/',
                    help='directory with named entity reconition dataset')

parser.add_argument('--output_dir', dest='output_dir' , type=str,
                    default='../out/',
                    help='directory where outputs are written')

args = parser.parse_args()

#TODO
#Check if dir end with /

cmd = ('python3 run_ner.py'
      ' --do_train=true'
      ' --do_eval=true'
      ' --vocab_file=' + args.biobert_dir + 'vocab.txt'
      ' --bert_config_file=' + args.biobert_dir + 'bert_config.json'
      ' --init_checkpoint=' + args.biobert_dir + 'model.ckpt-1000000'
      ' --num_train_epochs=1'
      ' --data_dir=' + args.ner_dir +
      ' --output_dir='  + args.output_dir)

os.chdir('./biobert')
os.system(cmd)

