# Medical entity extraction
This repository provides the code for fine-tuning and serving BioBERT. An adapted version of the BioBERT repository is included.


## Download
Below you can find a download link with necessary data. The data folder contains:
* BioBERT pretrained parameters and config (provided by BioBERT)
* Datasets for medical entity extraction
* Tensorflow SavedModels of finetuned BioBERT on NCBI and BC4CHEMD
* Data for demonstrations (PDFs)

https://drive.google.com/file/d/1wX14V5K10QWGEmw7h1iVUwr9VSVyI5aG/view?usp=sharing

Extra information on the content of data can be found below under section "Extra information on data"

## Installation
This section describes the steps for installation to be able to run the training and demo.

Extract the downloaded data folder into `data`, at the root of the repository

Install the requirements in requirements.txt

Install tensorflow-model-server with the following commands:

```bash
$ echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list

$ curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -

$ sudo apt-get update && sudo apt-get install tensorflow-model-server
```

## Instructions for training
Training can be started by running `train.py`. `train.py` accepts optional arguments for
--biobert_dir , --ner_dir , --ckpt_file and --output_dir . The default values start a training on NCBI dataset with pretrained BioBERT parameters. When training is finished, checkpoints, eval_results and
a Tensorflow SavedModel can be found in the output directory.

## Instructions for the demo
The demo is started by running `run_demo.py`. The demo can be shown in a browser under port 5000,
reachable by going to http://localhost:5000/ . The demo lets you choose between type of entity extraction and
will let you upload a pdf. In `data/demo_sample` 4 example pdfs are given.

## Extra information on data

In the folder `demo_sample` 3 examples of a medical exam can be found as pdf.

In the folder `NERdata` 8 datasets for named entity recognition are stored:
* Diseases: NCBI-disease BC5CDR-disease
* Drug/Chem.: BC5CDR-chem, BC4CHEMD
* Gene/protein: BC2GM, JNLPBA
* Species: linnaeus, s800

In the folder `pre_training` the v1.1 pubmed bioBert pre-trained parameters are stored, together with the bert_config.json

In the folder SavedModels, 2 folders with Tensorflow SavedModels are stored. One folder with models trained on BC4CHEMD and one folder with models trained on NCBI. The folders contain version-folders of the models. The demo-app selects the newest version of a model by default. The demo-app can be extended by training on the other datasets and adding the resulting SavedModels in this folder. Below the evaluations results of the `./biobert/biocodes/conlleval.pl` on the most recent SavedModels are listed.

BC4CHEMD:

```bash
processed 124316 tokens with 3914 phrases; found: 3882 phrases; correct: 3605.
accuracy:  99.28%; precision:  92.86%; recall:  92.11%; FB1:  92.48
             MISC: precision:  92.86%; recall:  92.11%; FB1:  92.48  3882

```

NCBI-disease

```bash
processed 24497 tokens with 960 phrases; found: 946 phrases; correct: 832.
accuracy:  98.69%; precision:  87.95%; recall:  86.67%; FB1:  87.30
             MISC: precision:  87.95%; recall:  86.67%; FB1:  87.30  946

```

