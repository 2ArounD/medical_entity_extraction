import requests
import json
import sys
import pdb

from flask import Flask, render_template, request

sys.path.insert(1, '../biobert')
import tokenization


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
    if request.method == 'POST':
        example = request.form['rawtext']

        endpoints = "http://localhost:9001/v1/models/BioBert:predict"
        headers = {"content-type":"application-json"}
        tokenizer = tokenization.FullTokenizer(vocab_file="../data/pre_training/biobert_v1.1_pubmed/vocab.txt",do_lower_case=True)
        token_a = tokenizer.tokenize(example)
        tokens = []
        tokens.append("[CLS]")
        segment_ids = []
        segment_ids.append(0)
        for token in token_a:
            tokens.append(token)
            segment_ids.append(0)
        tokens.append('[SEP]')
        segment_ids.append(0)
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(input_ids)
        max_seq_length = 256
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)

        label_id = 0
        instances = [{"input_ids":input_ids, "input_mask":input_mask, "segment_ids":segment_ids, "label_ids":label_id}]
        data = json.dumps({"signature_name":"serving_default", "instances":instances})
        response = requests.post(endpoints, data=data, headers=headers)

        print('response')
        print(response)
        print('end')
        prediction = json.loads(response.text)['predictions']
        print(prediction)

        pdb.set_trace()

        return render_template("index.html",results=prediction,num_of_results = 'num_of_results')


    return render_template("index.html",results='results',num_of_results = 'num_of_results')


if __name__ == '__main__':
    app.run(debug=True)
