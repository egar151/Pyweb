
from shelljob import proc
import os
from flask import Flask, render_template, request, redirect, Response, send_file
from datetime import datetime
import script
import eventlet
eventlet.monkey_patch()


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')
@app.route('/submit/', methods=['GET','POST'])
def my_link():
  date = request.form.get("date")
  date_object = datetime.strptime(date, '%Y-%m-%d').date()
  text = date_object.strftime("%m-%d-%Y")
  full_text = "NDATE=" + text
  x = script.find_replace("demo.dat","NDATE=",full_text)
  
  if x: 
    return redirect("/step2", code=302)
    
  else:
    return "Script Exited with 1"

@app.route('/step2')
def step2():
  return render_template('step2.html')

@app.route('/submit2')
def submit2():
  return os.system(f"ping -c 3 10.0.0.3")

@app.route( '/stream' )
def stream():
    g = proc.Group()
    p = g.run( [  'ping', '-c 4', '10.0.0.3' ] )

    def read_process():
        while g.is_pending():   
            lines = g.readlines(timeout=2.0)
            for proc, line in lines:
                yield line.decode('utf-8') + '\n'

    return Response( read_process(), mimetype= 'text/html' )

@app.route('/page')
def get_page():
    return send_file('page.html')


if __name__ == '__main__':
  app.run(debug=True)