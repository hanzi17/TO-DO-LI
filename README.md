# 개굴리: to-do-list 웹페이지

## 팀원
김용빈 ENTJ

양진혁 ISFP

전하영 INFJ

한지현 ISTP

## 배포주소
http://todoli.eba-etyihryg.ap-northeast-2.elasticbeanstalk.com/

## 프로젝트 소개
항해99 사전 프로젝트로 본 과정을 진행하기 이전에 진행하는 웹페이지 제작 미니 프로젝트로, 나만의 to-do-list를 작성하고 관리하는 서비스 프로젝트

## 시작 가이드
### 요구 사항

### 설치 
$ git clone https://github.com/hanzi17/todo-list-15.git

$ pip install flask pymongo bson dnspython

## 기술 스택
### Environment
Visual Studio Code, Git, GitHub
### Development
JavaScript, Python, HTML5, CSS3, Ajax, Jquery, Flask
### Communication
Slack, Gather

## 주요 기능
### *app.py

### login()
웹페이지에서 받아 온 아이디, 닉네임, 비밀번호 데이터를 MongoDB에 저장

### todo_post()
웹페이지에서 받아온 to-do-list를 MongoDB에 저장

### todo_done()
웹페이지 상에서 to-do-list 완료를 체크할 때 데이터 변환 및 alert 

### todo_cancel()
웹페이지 상에서 X 표시를 눌러 to-do-list를 삭제했을 때 MongoDB에서 데이터 삭제 및 alert

### user_int()
MongoDB user 테이블의 userInt 값을 가져옴

### todo_get()
위의 함수를 통해 가져온 userInt 값을 todo 테이블의 userInt 값과 비교하여 매칭 후 로그인

----------------

### *login.html

### login()
웹페이지를 통해 입력 받은 데이터 저장

----------------

### *index.html

### show_todo()
웹페이지를 통해 받은 to-do-list 데이터 가져오기

### save_todo()
to-do-list 데이터 MongoDB에 저장

### done_todo()
to-do-list 완료시 체크

### cancel_todo()
to-do-list 완료 체크 된 항목 취소

### delete_todo()
to-do-list 삭제

### renderCurrentWeather()
실시간 날씨 데이터 불러오기

### logout()
로그아웃 버튼 클릭시 로그인 페이지로 이동
