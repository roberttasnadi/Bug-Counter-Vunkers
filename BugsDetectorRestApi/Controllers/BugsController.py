from flask import Flask, request
from ApplicationServices.BugsAppService import imageProcessRequest
import json
app = Flask(__name__)

# localhost:5000/processImage?path=xxxxxx

class ResponseJson (object) :
    def __init__(self, fly, bigMosquito, normalMosquito, tinyMosquito):
        self.fly = fly
        self.tinyMosquito = tinyMosquito
        self.bigMosquito = bigMosquito
        self.normalMosquito = normalMosquito

@app.route('/processImage')
def processImage():
    path = request.args.get("path")
    bugsList = imageProcessRequest(path)
    data = ResponseJson(bugsList[0], bugsList[1], bugsList[2], bugsList[3])
    return json.dumps(data.__dict__)

if __name__ == '__main__':
    app.run()
    app.run(host="0.0.0.0")
