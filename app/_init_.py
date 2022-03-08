from flask import Flask
import job
from flask import request
app = Flask(__name__)
@app.route("/", methods=['POST'])
def hello():
    return "Hello, World!"

@app.route("/job", methods=['POST'])
def jobSearch():
    insertValues = request.get_json()
    x1=insertValues['career']
    print(x1)
    job.getJob(x1)
    return "Done!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
