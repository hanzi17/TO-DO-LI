from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from bson.objectid import ObjectId

from pymongo import MongoClient 
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:JEix6NjqkUe2HlnI@cluster0.dx5eieg.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    userInt_receive = request.cookies.get('userInt')
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')


# 몽고DB에 닉네임, 이메일, 비밀번호 데이터 넣기
@app.route("/login", methods=["POST"])
def login():
    userInt = 0
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']
    
    doc = {
        'userInt': userInt,
        'id': id_receive,
        'pw': pw_receive,
        'nickname' : nick_receive,
    }
    userInt += 1 

    # id, 암호화된 pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_receive, 'nickname': nick_receive})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:

        # token을 줍니다.
        return jsonify({'result': 'success', 'nickname': result['nickname']})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



# 몽고DB에 to-do-list 데이터 넣기
@app.route("/todo", methods=["POST"])
def todo_post():
    date_receive = request.form['date_give']
    list_receive = request.form['list_give']

    doc = {
        'date': date_receive,
        'list': list_receive,
        'done' : 0
    }
    db.todo.insert_one(doc)
    return jsonify({'msg': '입력 완료!'})


#투두 리스트 완료 체크할 때
@app.route("/todo/done", methods=["POST"])
def todo_done():
    id_receive = request.form['id_give']
    db.todo.update_one({'_id': ObjectId(id_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '완료!'})

#투두 완료 취소 
@app.route("/todo/cancel", methods=["POST"])
def todo_cancel():
    id_receive = request.form['id_give']
    db.todo.update_one({'_id': ObjectId(id_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '완료 취소!'})

#투두 삭제
@app.route("/todo/delete", methods=["POST"])
def todo_delete():
    id_receive = request.form['id_give']
    db.todo.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({'msg': '삭제 완료'})


#몽고디비에서 num 값 대신 DB 고유값인 ID값 가져오기
#ID를 가져오는 이유는 완료 표시를 하기 위해서!
@app.route("/todo", methods=["GET"])
def todo_get():
    userInt_receive = request.cookies.get('userInt')
    userinfo = db.user.find_one({'userInt': userInt_receive})

    todo_memo_list = list(db.todo.find({}))

    for i in range(len(todo_memo_list)):
        todo_memo_list[i]['_id'] = str(todo_memo_list[i]['_id'])
    return jsonify({'todo_memos': todo_memo_list, 'userIntNum':userinfo})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)    
