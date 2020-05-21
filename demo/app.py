from flask import Flask,render_template,url_for,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
    if request.method == 'POST':
        pass
        #Implement BIOBERT entity extraction


    return render_template("index.html",results='results',num_of_results = 'num_of_results')


if __name__ == '__main__':
    app.run(debug=True)
