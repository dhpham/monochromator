from flask import Flask, request, render_template, redirect, jsonify
# import main

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/control', methods = ['GET', 'POST'])
def control():
    return render_template('control.html')

@app.route('/do_steps', methods = ['POST'])
def do_steps():
    steps = int(request.form['steps'])
    direction = bool(int(request.form['dir']))
    delay = float(request.form['delay'])
    microstep = int(request.form['ms'])

    # main.do_Steps(steps,direction,delay,microstep)

    r = {}
    r['steps'] = steps
    r['direction'] = direction
    r['delay'] = delay
    r['microstep'] = microstep

    return jsonify(r)

@app.route('/do_obs', methods = ['GET', 'POST'])
def do_obs():
    # main.do_Obs()
    return True

@app.route('/calibrate', methods = ['GET', 'POST'])
def calibrate():
    # main.calibrate()
    return True

@app.route('/spectrum', methods = ['GET', 'POST'])
def spectrum():
    return render_template('spectrum.html')

@app.route('/go_home', methods = ['GET', 'POST'])
def go_home():
    # main.go_Home()
    return True

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)

