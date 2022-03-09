from flask import Flask
import job
from flask import request
app = Flask(__name__)
@app.route("/test", methods=['POST'])
def hello():
    return "Hello, World!"

@app.route("/job", methods=['POST'])
def jobSearch():
    insertValues = request.get_json()
    x1=insertValues['career']
    print(x1)
    job.getJob(x1)
    return "Done!"
