from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/text', methods = ['POST'])
def hello():
    s = request.form['textbox']
    return render_template('text.html', text=s)

@app.route('/refresh', methods = ['GET'])
def refresh():
    return render_template('refresh.html', f=1)

@app.route('/control', methods = ['GET'])
def control():
    return render_template('control.html')

@app.route('/stepper', methods = ['POST'])
def stepper():
    steps = int(request.form['steps'])
    delay = float(request.form['delay'])
    direction = str(request.form['dir'])
    microstep = int(request.form['ms'])

    r = {}
    r['steps'] = steps
    r['delay'] = delay
    r['direction'] = direction
    r['microstep'] = microstep

    return jsonify(r)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
