from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

Hobby = {
    "sports" : ["Sports"], 
    "music" : ["Music"],
    "cooking" : ["Gourment", "Slice of life"],
    "gaming" : ["Game", "Sci-fi", "Action", "Advanture"],
    "reading" : ["Mystery", "Fantasy"],
    "technology" : ["Sci-fi", "Mecha"],
    "dancing" : ["Music"],
}
@app.route("/")
def hello_world():
    return "Hello world"

if __name__ == '__main__':
    
    app.run(debug = True)