# Medical entity extraction
This repository provides the code for fine-tuning BioBERT, an adapted version of the BioBERT repository is included.
Please refer to our paper  for more details.
This project is done by [DMIS-Lab](https://dmis.korea.ac.kr).

## Download
Below you can find a download with necessary data. The data folder contains;
* BioBERT pretrained parameters and config (provided by BioBERT)
* Datasets for medical entity extraction
* Tensorflow SavedModels of finetuned BioBERT on NCBI and BC4CHEMD
* Data for demonstrations (PDFS)

Extra information on the content of data can be found below under "Extra information on data"

## Installation
This section describes the steps for installation to be able to run the training and demo.

Extract the downloaded data folder into `data`

Install the requirements in requirements.txt

Install tensorflow-model-server with the following commands:

`echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list`
`curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -`
`sudo apt-get update && sudo apt-get install tensorflow-model-server`

## Instructions for training
Training can be started by running `train.py`. `train.py` accepts optional arguments for
--biobert_dir , --ner_dir , --ckpt_dir and --output_dir . By default the training is started using
BioBERT pretrained parameters on the NCBI disease dataset. After training ckpts, eval_results and
a Tensorflow SavedModel can be found in --output_dir.

## Instructions for demo
The demo is started by running `run_demo.py`. The demo can be shown in a browser under port 5000,
reachable by going to http://localhost:5000/ . The demo lets you choose between type of entity extraction and
will let you upload a pdf. In data/demo_sample 4 example pdfs are given.

## Extra information on data

## Citation
```
@article{10.1093/bioinformatics/btz682,
    author = {Lee, Jinhyuk and Yoon, Wonjin and Kim, Sungdong and Kim, Donghyeon and Kim, Sunkyu and So, Chan Ho and Kang, Jaewoo},
    title = "{BioBERT: a pre-trained biomedical language representation model for biomedical text mining}",
    journal = {Bioinformatics},
    year = {2019},
    month = {09},
    issn = {1367-4803},
    doi = {10.1093/bioinformatics/btz682},
    url = {https://doi.org/10.1093/bioinformatics/btz682},
}
```
