from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = b'random string...'

name_list = {}
message_data =[]

@app.route('/', methods=['GET'])
def index():
   global name_list
   global message_data

   title ="메시지"
   msg = "Flask"

   if 'flag' in session and session['flag']:
       flag = session['flag']
       msg = '로그인ID：' + session['id']
       user_id = session['id']

       return render_template('message.html', \
               title='게시판 page', \
               message=msg,\
               name = name_list,\
               user_id = user_id,\
               flag = flag,\
               session = session,\
               data = message_data)
   else:
       return redirect('/login')

@app.route('/', methods=['POST'])
def message():
  msg = request.form.get('comment')
  message_data.append((session['id'],msg))

  return redirect('/')


@app.route('/login', methods=['GET'])
def login():
   global name_list

   title ="메시지"
   msg = "로그인해주시면 post를 작성 가능합니다"

   return render_template('login.html', \
               title='로그인 해주세요', \
               message=msg,
               name = name_list)

@app.route('/login' , methods=['POST'])
def login_post():
   global name_list

   id = request.form.get('id')
   pwd = request.form.get('pass')

   #idが既にあるかどうかを確認する
   if id in name_list:
       #IDとpasswordが一致しているかを確認する。
       if pwd == name_list[id]:
           #ログイン可能な状態にする
           session['flag'] = True
       #IDとpasspwrdが一致しない場合は
       else:
           session['flag'] = False
   #idの新規登録の場合
   else:
       name_list[id] = pwd
       session['flag'] = True #ログイン可能な状態にする

   session['id'] = id
   user_id = session.get("id")
   flag = session['flag']
   #idとpasseprdが一致するかどうかの確認
   if session['flag']: #一致した場合
       return redirect('/')

   else: #一致しなかった場合
       title = '로그인'
       msg = '잘 못 한 password 입니다'

       return render_template('login.html',\
           title = title,\
           message = msg,\
           name = name_list,\
           user_id=user_id,
           flag = flag)

@app.route('/logout',methods=['GET'])
def logout():
   session.pop('id',None)
   session.pop('flag')
   return redirect('/')

@app.route('/delete',methods=['GET'])
def delete():
   global message_data
   message_data =[]
   return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
   app.run(debug=True)

