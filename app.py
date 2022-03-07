from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import config

from pymongo import MongoClient
client = MongoClient(config.mongoDB)
db = client.dbsparta
# 개인별 몽고DB를 기입해 주셔야 합니다.

@app.route('/')
def home():
    return render_template('index.html')

#  지역별 필터 기능
@app.route("/mnt_select", methods=["GET"])
def mnt_select():
    doc = []  # 검색을 마친 자료가 들어갈 배열입니다.
    area_receive = request.args.get("area_give")
    mountains = list(db.mnt_info.find({}, {'_id': False}))  # 산의 전체 목록을 mountains 변수로 받아옵니다.
    for mountain in mountains:
        if area_receive in mountain['mnt_address']:  # 산의 세부 설명에서 mnt_receive로 받은 검색어를 찾아봅니다.
            doc.append(mountain)  # 일치하는 명산의 번호를 doc 배열에 집어넣습니다.
    return jsonify({'search_list': doc, 'msg': '검색완료!'})

# index_sub로 연결하면서 mnt_no 데이터를 전송
@app.route('/index_sub', methods=['GET'])
def index_sub():
    mnt_no = request.args.get('mnt_no')
    return render_template('index_sub.html', mnt_no = mnt_no)

@app.route("/mnt_info", methods=["GET"])
def mnt_get():
    all_mnt = list(db.mnt_info.find({},{'_id':False}))
    return jsonify({'mnt': all_mnt})

@app.route("/mnt_show", methods=["GET"])
def show_mnt():
    num_receive = request.args.get('num_give')
    mnt_data = db.mnt_info.find_one({'mnt_no':int(num_receive)},{'_id':False})
    return jsonify({'mnt_data': mnt_data})

@app.route("/show_comment", methods=["GET"])
def show_comment():
    mnt_no = request.args.get('num_give')
    mnt_data = db.mnt_info.find_one({'mnt_no':int(mnt_no)},{'_id':False})
    if 'comments' in mnt_data:
        return jsonify({'mnt_data': mnt_data['comments']})
    else:
        return jsonify({'msg': '코멘트가 없습니다.'})

@app.route('/save_comment', methods=['POST'])
def save_comment():
    num_receive = request.form['num']
    name_receive = request.form['name']
    comment_receive = request.form['comment']
    score_receive = request.form['score']
    # if문이 계속 반복되므로 좋은 코딩은 아니라고 합니다. 더 좋은 방법을 알고 계신다면 피드백 부탁드립니다.
    if not name_receive.strip():
        return jsonify({'denied': '이름을 입력해주세요!'})
    if not comment_receive.strip():
        return jsonify({'denied': '내용을 입력해주세요!'})
    if score_receive == '별점':
        return jsonify({'denied': '별점을 선택해주세요!'})

    arr = []
    doc = {'name': name_receive, 'comment': comment_receive, 'score': int(score_receive)}
    arr.append(doc)

    mnt_data = db.mnt_info.find_one({'mnt_no':int(num_receive)})
    if 'comments' in mnt_data:
        mnt_data['comments'].append(doc)
        db.mnt_info.update_one({'mnt_no': int(num_receive)}, {'$set': {'comments': mnt_data['comments']}})
        return jsonify({'success': '등록완료!'})
    else:
        print(mnt_data)
        db.mnt_info.update_one({'mnt_no': int(num_receive)}, {'$set': {'comments': arr}})
        return jsonify({'success': '등록완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
