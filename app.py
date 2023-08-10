from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from bson.objectid import ObjectId


# 파이몽고 연결하기
from pymongo import MongoClient
client = MongoClient('mongodb+srv://pmaker126:test@cluster0.pemxrix.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


# 몽고DB에 닉네임, 이메일, 비밀번호 데이터 넣기
@app.route("/login", methods=["POST"])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.todo.find_one({'email': id_receive, 'pw': pw_receive, 'nick': nick_receive})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:

        # token을 줍니다.
        return jsonify({'result': 'success'})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



# (POST) 몽고DB에 투두 넣기
@app.route("/todo", methods=["POST"])
def todo_post():
    date_receive = request.form['date_give']  # 클라이언트에서 날짜 정보를 가져와서 date_receive에 넣음
    list_receive = request.form['list_give']  # 클라이언트에서 투두 정보를 가져와서 list_receive에 넣음

    doc = {  # 몽고DB에 저장되는 키와 밸류값
        'date': date_receive,
        'list': list_receive,
        'done' : 0 # 0은 미완료, 1은 완료 / 처음에 투두 넣을때는 전부 0으로 들어감
    }
    db.todo.insert_one(doc)
    return jsonify({'msg': '입력 완료!'})  # 다 넣으면 '입력 완료' 메시지 반환



# (POST) 완료 투두 처리
@app.route("/todo/done", methods=["POST"])
def todo_done():
    id_receive = request.form['id_give']  # 클라이언트에서 받은 체크박스 onclick=done_todo의 아이디값(=투두의 고유 ID값)
    db.todo.update_one({'_id': ObjectId(id_receive)}, {'$set': {'done': 1}})
    # id값을 투두 컬렉션에 업데이트함
    # '_id' 필드는 MongoDB에서 자동으로 생성되는 고유한 식별자인데, 이를 사용하여 문서를 식별
    # ObjectId(id_receive)는 클라이언트 측에서 전달받은 할 일의 ID를 MongoDB의 ObjectID 타입으로 변환하여 사용하는 것
    # {'$set': {'done': 1}}: 업데이트할 내용
    # '$set' 연산자를 사용하여 해당 문서의 'done' 필드를 1로 설정 = 투두 완료
    return jsonify({'msg': '완료!'})



# (POST) 완료취소 투두 처리
@app.route("/todo/cancel", methods=["POST"])
def todo_cancel():
    id_receive = request.form['id_give']  # 클라이언트에서 받은 체크박스 onclick=cancel_todo의 아이디값(=투두의 고유 ID값)
    db.todo.update_one({'_id': ObjectId(id_receive)}, {'$set': {'done': 0}})
    # id값을 투두 컬렉션에 업데이트함
    # '_id' 필드는 MongoDB에서 자동으로 생성되는 고유한 식별자인데, 이를 사용하여 문서를 식별
    # ObjectId(id_receive)는 클라이언트 측에서 전달받은 할 일의 ID를 MongoDB의 ObjectID 타입으로 변환하여 사용하는 것
    # {'$set': {'done': 0}}: 업데이트할 내용
    # '$set' 연산자를 사용하여 해당 문서의 'done' 필드를 0로 설정 = 투두 미완료
    return jsonify({'msg': '완료 취소!'})



# (POST) 삭제 투두 처리
@app.route("/todo/delete", methods=["POST"])
def todo_delete():
    id_receive = request.form['id_give']  # 클라이언트에서 받은 버튼 onclick=delete_todo의 아이디값(=투두의 고유 ID값)
    db.todo.delete_one({'_id': ObjectId(id_receive)})
    # id값을 투두 컬렉션에서 삭제함
    # '_id' 필드는 MongoDB에서 자동으로 생성되는 고유한 식별자인데, 이를 사용하여 문서를 식별
    # ObjectId(id_receive)는 클라이언트 측에서 전달받은 할 일의 ID를 MongoDB의 ObjectID 타입으로 변환하여 사용하는 것
    return jsonify({'msg': '삭제 완료'})



# (GET) 몽고DB에서 투두 id 조회 > 클라이언트에 보내기
@app.route("/todo", methods=["GET"])  # 클라이언트가 /todo 에 GET 요청을 보내면 todo_get() 함수를 실행
def todo_get():
    todo_memo_list = list(db.todo.find())  # 몽고DB의 "todo" 컬렉션에서 모든 문서들을 가져와 리스트 형태로 todo_memo_list 변수에 저장

    for i in range(len(todo_memo_list)):  # 가져온 투두들의 개수만큼 반복 / range(10) = 0~9
        todo_memo_list[i]['_id'] = str(todo_memo_list[i]['_id'])  # 각 투두의 내부값 중 '_id'은 문자열로 전달하기
    return jsonify({'todo_memos': todo_memo_list})  # 클라이언트와 이어져있는 'todo_memos' 에 가져온 투두들 보내기



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)