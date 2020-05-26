import os
import argparse

#Argument parsing, mainly to control starting checkpoint and dataset
#Per default training starts on NCBI with standard biobert weights
parser = argparse.ArgumentParser()
parser.add_argument('--biobert_dir', dest='biobert_dir' , type=str,
                    default='../data/pre_training/biobert_v1.1_pubmed/',
                    help='directory with biobert pretrained weights, config and vocab')

parser.add_argument('--ner_dir', dest='ner_dir' , type=str,
                    default='../data/NERdata/NCBI-disease',
                    help='directory with named entity reconition dataset/')

parser.add_argument('--ckpt_dir', dest='ckpt_dir' , type=str,
                    default='../data/pre_training/biobert_v1.1_pubmed/',
                    help='directory where ckpts for resuming training are stored')

parser.add_argument('--output_dir', dest='output_dir' , type=str,
                    default='../out/',
                    help='directory where outputs are written')

args = parser.parse_args()

# Command to start training/eval/prediction
# eval, predict and SavedModel need a model in output directory
# If no training is required from given ckpt, easiest fix is to train for 0.01 epochs
# Otherwise provide model in out_dir

cmd = ('python3 run_ner.py'
       ' --do_train=true'
       ' --do_eval=true'
       ' --do_predict=false'
      ' --vocab_file=' + args.biobert_dir + 'vocab.txt'
       ' --bert_config_file=' + args.biobert_dir + 'bert_config.json'
       ' --init_checkpoint=' + args.ckpt_dir +
       ' --num_train_epochs=5' +
       ' --data_dir=' + args.ner_dir +
       ' --output_dir='  + args.output_dir +
       ' --create_SavedModel=true')  # create_SavedModel as true will set do_predict to false
                                     # Needs better fix in run_ner.py (line 414 & 506)

os.chdir('./biobert')
os.system(cmd)

