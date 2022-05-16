from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, url_for, request, redirect, flash, jsonify
from flask import render_template
from flask_socketio import SocketIO, emit
# from gevent.pywsgi import WSGIServer
from config import *
import mc
import os
import logging
import datetime
import time


logging.basicConfig(filename=LOGFILENAME, level=logging.INFO)
app = Flask(__name__)
app.secret_key = os.urandom(64)
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '登入成功'


def wrlog(request, statement: str) -> None:
    admin_ip = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    current_time = str(datetime.datetime.now().astimezone(TIMEZONE))
    seconds = str(time.time())
    logging.info(','.join([statement, admin_ip, current_time, seconds]))


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(account):
    if account not in USERS:
        return
    user = User()
    user.id = account
    return user


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        logging.info("LOGIN username: " + username +
                     ", password: " + request.form['password'])
        if username in USERS:
            if request.form['password'] == USERS[username]['password']:
                #  實作User類別
                user = User()
                #  設置id就是email
                user.id = username
                #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。
                login_user(user)
                logging.info('LOGIN successful')
                return redirect('controller')
            else:
                pass
        logging.info('LOGIN Failed!!!')
        return redirect('login')


@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'


@app.route('/controller', methods=['GET'])
@login_required
def controller():
    if current_user.is_active:
        is_online = mc.is_online()
        status = mc.status()
        players_num = (status.online if status != None else 0)
        max_players = (status.max if status != None else 'Unknown')
        account_list = mc.online_account()
        return render_template('controller.html', is_online=is_online, players_num=players_num, account_list=account_list, max_players=max_players)
    return redirect('login')



@app.route('/startserver', methods=['GET'])
@login_required
def startserver():
    if current_user.is_active:
        wrlog(request, 'startserver')
        mc.start()
        result = {'state': 'success', 'data': {}}
        return jsonify(result)
    return redirect('/')


@app.route('/stopserver', methods=['GET'])
@login_required
def stopserver():
    if current_user.is_active:
        wrlog(request, 'stopserver')
        mc.stop()
        result = {'state': 'success', 'data': {}}
        return jsonify(result)
    return redirect('/')


@socketio.on('send')
def chat(data):
    socketio.emit('get', data)


@socketio.on('test')
def test():
    socketio.send("test")


if __name__ == '__main__':
    # http_server = WSGIServer((Web.HOST, Web.PORT), app)
    # http_server.serve_forever()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run(debug=True, host='localhost')
    socketio.run(app, host=Web.HOST, port=Web.PORT, debug=True)
