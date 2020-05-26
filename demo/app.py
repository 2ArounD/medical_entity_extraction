import requests
import json
import sys
import os
import textract

from flask import (Flask, render_template, request, flash, redirect,
                   send_from_directory)
from flaskext.markdown import Markdown
from werkzeug.utils import secure_filename
from templates.templates import HTML_WRAPPER, TPL_MARKUP_WRAPPER, TPL_MARKPUP

sys.path.insert(1, '../biobert')
import tokenization

UPLOAD_FOLDER = './demo_uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
Markdown(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template("index.html", result='')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        choice = request.form['taskoption']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Extract all the text from the pdf
            raw_text = textract.process(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Select model and entity-tag depending on choice user
            if choice == 'Diseases and symptoms':
                endpoints = "http://localhost:9001/v1/models/BioBert:predict"
                tag = 'Disease/symptom'
            if choice == 'Drugs and chemicals':
                endpoints = "http://localhost:8501/v1/models/BioBert:predict"
                tag = 'Drug/chemical'
            headers = {"content-type":"application-json"}

            # Process text to generate predictions and create html markup
            predictions, tokens = get_prediction(raw_text, endpoints, headers)
            html = create_markup(predictions, tokens, tag)
            html = html.replace("\n\n","\n")
            result = HTML_WRAPPER.format(html)

            return render_template('index.html', result=result)

    return render_template("index.html", result='')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_prediction(raw_text, endpoints, headers):
    # This function loops trough the raw text, splits the text in tokenized
    # lines and generated predictions based on the tokenized lines.
    # The predictions per token in line and tokens are returned

    # Convert ful text into tokens
    tokenizer = tokenization.FullTokenizer(vocab_file="../data/pre_training/biobert_v1.1_pubmed/vocab.txt",do_lower_case=True)
    token_a = tokenizer.tokenize(raw_text)

    # Loop through all tokens, splitting them in lines
    # The tokens_lines are added to list tokens_text
    # tokens_lines are also converted to input_ids for biobert

    counter = 0
    tokens_line = []
    tokens_text = []
    input_ids = []

    tokens_line.append("[CLS]")
    for token in token_a:
        if token == '.':
            tokens_line.append("[SEP]")
            tokens_text.append(tokens_line)
            input_ids.append(tokenizer.convert_tokens_to_ids(tokens_line))
            tokens_line = []
            tokens_line.append("[CLS]")
            counter = 0

        # lines are cut of when they surpass 110 tokens
        elif counter > 110:
            # lines are not cut off when in the middle of a word
            if not token[:2] == '##':
                tokens_line.append("[SEP]")
                tokens_text.append(tokens_line)
                input_ids.append(tokenizer.convert_tokens_to_ids(tokens_line))
                tokens_line = []
                tokens_line.append("[CLS]")
                counter = 0
        tokens_line.append(token)

        counter = counter + 1

    tokens_line.append('[SEP]')
    input_ids.append(tokenizer.convert_tokens_to_ids(tokens_line))
    tokens_text.append(tokens_line)

    # Lines shorter than max length are appended with zeros
    max_seq_length = 128
    for input_id in input_ids:
        while len(input_id) < max_seq_length:
            input_id.append(0)

    # Dummy input for input_mask, segment_ids and label_id
    input_mask = [1] * max_seq_length
    segment_ids = [0] * max_seq_length
    label_id = 0

    # Loop through lines of input_ids and make predictions
    predictions = []
    for input_id in input_ids:
        instances = [{"input_ids":input_id, "input_mask":input_mask, "segment_ids":segment_ids, "label_ids":label_id}]
        data = json.dumps({"signature_name":"serving_default", "instances": instances})
        response = requests.post(endpoints, data=data, headers=headers)
        predictions.append(json.loads(response.text)['predictions'][0]['predict'])

    return predictions, tokens_text


def detokenize(prediction, tokens):
    # Adapted version of biobert detokenize function
    # Converts prediction mapped on tokens to prediction mapped on words

    pred = {'toks': [], 'labels': []}  # dictionary for predicted tokens and labels.
    for idx, (tok, lab) in enumerate(zip(tokens, prediction)):
        tok = tok.strip()
        pred['toks'].append(tok)

        pred['labels'].append(lab)

    labeled_words = {'toks': [], 'labels': [], 'sentence': []}
    buf = []
    for t, l in zip(pred['toks'], pred['labels']):
        if t in ['[CLS]', '[SEP]']:  # non-text tokens will not be evaluated.
            labeled_words['toks'].append(t)
            labeled_words['labels'].append(t)  # Tokens and labels should be identical if they are [CLS] or [SEP]
            if t == '[SEP]':
                labeled_words['sentence'].append(buf)
                buf = []
            continue
        elif t[:2] == '##':  # if it is a piece of a word (broken by Word Piece tokenizer)
            labeled_words['toks'][-1] += t[2:]  # append pieces to make a full-word
            buf[-1] += t[2:]
        else:
            labeled_words['toks'].append(t)
            labeled_words['labels'].append(l)
            buf.append(t)

    return labeled_words


def create_markup(predictions, tokens_list, tag):
    # Function to create html markup to highlight words based on their labels

        markup = ''

        # Loop through each line in prediction
        for pred_idx, pred in enumerate(predictions):
            labeled_words = detokenize(pred, tokens_list[pred_idx])
            words_line = labeled_words['toks']
            labels_line = labeled_words['labels']
            m_add = ''
            marking_done = True

            # Loop through line, add highlight to entities
            for idx, word_raw in enumerate(words_line):
                word = escape_html(word_raw)  # replace signs interferring with html
                if labels_line[idx] == 1:  # Start of entity
                    m_add = word
                    marking_done = False
                elif labels_line[idx] == 2:  # Optional continuiation of entity
                    m_add = m_add + ' ' + word
                elif labels_line[idx] == '[CLS]':
                    pass
                elif labels_line[idx] == '[SEP]':
                    pass
                else:
                    if not marking_done:  # Add highlighted entity if end entity is reached
                        markup += TPL_MARKPUP.format(label=tag, text=m_add, bg="#e4e7d2") ##9cc9cc
                        marking_done = True
                        m_add = ''
                    if len(markup) > 0:  # Improve readability of resulted markup
                        if word in ".,:/;'" or word in '"':
                            if markup[-1] == ' ':
                                markup = markup[:-1] + word + ' '
                            else:
                                markup += word + ' '
                        else:
                            markup += word + ' '
                    else:
                        markup += word + ' '

            if not marking_done:
                markup += TPL_MARKPUP.format(label=tag, text=m_add, bg="#e4e7d2")
                marking_done = True
            m_add = ''

        markup = TPL_MARKUP_WRAPPER.format(content=markup, dir='ltr')

        return markup


def escape_html(text):
    # Replace <, >, &, " with their HTML encoded representation. Intended to
    # prevent HTML errors in rendered displaCy markup.
    # text (unicode): The original text.
    # RETURNS (unicode): Equivalent text to be safely used within HTML.

    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text

if __name__ == '__main__':
    app.secret_key = 'key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=False)
