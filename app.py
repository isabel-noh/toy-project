from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://<id>:<pw>@cluster0.xkvvx.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/hiking", methods=["POST"])
def hiking_post():
    star_receive = request.form["star_give"]
    comment_receive = request.form["comment_give"]
    return jsonify({'msg':'등록 완료'})

@app.route("/hiking", methods=["GET"])
def hiking_get():
    review_list = list(db.hiking.find({}, {'_id': False}))
    return jsonify({'reviews':review_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)