from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/text', methods = ['POST'])
def hello():
    s = request.form['textbox']
    return render_template('text.html', text=s)



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
