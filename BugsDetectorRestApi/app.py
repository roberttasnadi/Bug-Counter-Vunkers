from flask import Flask
import cv2

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return "hola"

@app.route("/processImage")
def prova():
    return "asdasd"

if __name__ == '__main__':
    app.run()
