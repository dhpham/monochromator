from flask import Flask, request, render_template, redirect
# import main

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/control', methods = ['GET'])
def control():
    return render_template('control.html')

@app.route('/step_redir', methods = ['GET'])
def step_redir():
    steps = request.values['steps']
    direction = request.values['dir']
    delay = request.values['delay']
    microstep = request.values['ms']

    return render_template('step.html', \
        steps = steps, direction = direction, delay = delay, microstep = microstep)

@app.route('/do_steps', methods = ['GET'])
def do_steps():
    steps = int(request.values['steps'])
    direction = bool(int(request.values['dir']))
    delay = float(request.values['delay'])
    microstep = int(request.values['ms'])

    # main.do_Steps(steps,direction,delay,microstep)

    return redirect('/')

@app.route('/obs_redir', methods = ['GET'])
def obs_redir():
    return render_template('obs.html')

@app.route('/do_obs', methods = ['GET'])
def do_obs():
    # main.do_Obs()
    return redirect('/spectrum')

@app.route('/calibrate_redir', methods = ['GET'])
def calibrate_redir():
    return render_template('/calibrate.html')

@app.route('/calibrate', methods = ['GET'])
def calibrate():
    # main.calibrate()
    return redirect('/')

@app.route('/home_redir', methods = ['GET'])
def home_redir():
    return render_template('home.html')

@app.route('/go_home', methods = ['GET'])
def go_home():
    # main.go_Home()
    return redirect('/')

@app.route('/spectrum', methods = ['GET'])
def spectrum():
    return render_template('spectrum.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)

