from flask import Flask, render_template, request
from eiki import Eiki
import json
import waitress

devices = json.load(open("./config.json","r"))['devices']

app = Flask(__name__)
x = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/init")
def init():
    global devices
    for d in devices:
        devices[d]['obj'] = Eiki(ip=devices[d]['ip'],name=d)
    x.update(devices)
    return render_template("index.html")

@app.route("/get")
def get():
    for key in x:
        try:    
            x[key]['state'] = x[key]['obj'].state
            del(x[key]['obj'])
        except KeyError:
            pass
    return(json.dumps(x))

@app.route("/control", methods=['POST'])
def control():
    if(request.method == "POST"):
        try:
            name = request.args['name']
        except KeyError:
            return json.dumps({"message":"key error!"})
        try:
            device = devices[name]
            print(device)
            print(request.args)
            #device.control(command=(request.args['state']))
            return json.dumps({"success":1})
        except KeyError:
            return json.dumps({"message":"device not found!"})
        except Exception as e:
            print(type(e).__name__,e.args)
            return json.dumps({"message":"error!"})

if __name__ == '__main__':
    #x = discover()
    #waitress.serve(app,host="127.0.0.1",port=9999)
    app.run(host="0.0.0.0",debug=True)