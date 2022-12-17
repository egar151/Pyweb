
import os
from flask import Flask, render_template, request, redirect
from datetime import datetime
import script
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

if __name__ == '__main__':
  app.run(debug=True)