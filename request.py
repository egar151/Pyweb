
from shelljob import proc
import os
from flask import Flask, render_template, request, redirect, Response, send_file
from datetime import datetime
import script
import eventlet
eventlet.monkey_patch()


app = Flask(__name__)

##Show First WebPage with form and input.
@app.route('/')
def index():
  return render_template('index.html')

  
@app.route('/submit/', methods=['GET','POST'])

##Define Function
def my_link():
  ##Get post result from Name=date
  date = request.form.get("date")
  ## Format Date to the correct order, Year-month-day.
  date_object = datetime.strptime(date, '%Y-%m-%d').date()
  ## Change Date to String Format
  text = date_object.strftime("%m-%d-%Y")
  ## Add the Prefix to the Date.
  full_text = "NDATE=" + text
  
  ## Get Post Result from
  runid = "RUNID="+request.form.get("runid")
  
  ## Replace the desire line for Date and RUNID, which are in different files. Returns boolean result
  x = script.find_replace("demo.dat","NDATE=",full_text)
  y = script.find_replace("other.dat","RUNID=",runid) 

  ## Checks the output of the replace for errors.
  if x:
    if y: 
      ## If all true, redirect to Step 2 with error code 302. Using other codes will not make redirect automatically.
      return redirect("/step2", code=302)
    else:
      return "Script Exited with 2"
  else:
    return "Script Exited with 1"


## Step 2, has no use for now.
@app.route('/step2')
def step2():
  return render_template('step2.html')

## Part of Step 2, didnt work as expected.
@app.route('/submit2')
def submit2():
  return os.system(f"ping -c 3 10.0.0.3")


## Runs Commands on Shell and send result to browser.
@app.route( '/stream' )
def stream():
    g = proc.Group()
    p = g.run( [  'ping', '-c 10', '127.0.0.1' ] )
    def read_process():
        while g.is_pending():   
            lines = g.readlines(timeout=2.0)
            for proc, line in lines:
                yield line.decode('utf-8') + '<br/>'

    return Response( read_process(), mimetype= 'text/html' )


##Shows Webpage with iframe of /scream route.
@app.route('/page')
def get_page():
    return send_file('page.html')


if __name__ == '__main__':
  app.run(debug=True)