from flask import Flask, request, render_template, redirect, jsonify
# import main

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return redirect('/control', code=302)

@app.route('/control', methods = ['GET'])
def control():
    return render_template('control.html')

@app.route('/stepper', methods = ['POST'])
def stepper():
    # return redirect('/do_steps', code=307)

@app.route('/do_steps', methods = ['POST'])
def do_steps():
    steps = int(request.form['steps'])
    direction = bool(int(request.form['dir']))
    delay = float(request.form['delay'])
    microstep = int(request.form['ms'])

    # main.do_Steps(steps,direction,delay,microstep)

    r = {}
    r['steps'] = steps
    r['delay'] = delay
    r['direction'] = direction
    r['microstep'] = microstep

    return jsonify(r)

@app.route('/do_obs', methods = ['GET'])
def do_obs():
    pass

@app.route('/calibrate', methods = ['GET'])
def calibrate():
    pass

@app.route('/spectrum', methods = ['GET'])
def spectrum():
    pass

@app.route('/go_home', methods = ['GET'])
def go_home():
    pass

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)

