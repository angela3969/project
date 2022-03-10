from flask import Flask
import job
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/test", methods=['POST'])
def hello():
    return "Hello, World!"

@app.route("/job", methods=['POST'])
def jobSearch():
    insertValues = request.get_json()
    x1=insertValues['url']
    print(x1)
    job.getSkill(x1)
    return job.getSkill(x1)
