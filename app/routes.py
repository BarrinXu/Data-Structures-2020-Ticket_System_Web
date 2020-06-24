from app import app
from app.forms import RegisterForm, LoginForm, QueryUserForm, EditUserForm, AddTrainForm, ReleaseTrainForm, \
    DeleteTrainForm, QueryTrainForm, QueryTicketForm, BuyTicketForm
from app.models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

import subprocess as sp
import time
import fcntl
import os

path = './code'
echo = sp.Popen(path, stdin=sp.PIPE, stdout=sp.PIPE, universal_newlines=True)
fd = echo.stdout.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def com(s):
    data = str(s) + '\n'
    echo.stdin.write(data)
    echo.stdin.flush()
    time.sleep(1e-3)
    ret = ''
    while True:
        try:
            ret += os.read(fd, 1024).decode('utf-8')
        except:
            break
    return ret[:-1]


@app.route('/')
# @login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if (not current_user.is_authenticated) and False:  # 如果未登录&&数据库有用户
    #     flash('请先登录再添加新用户！', category='warning')
    #     return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:  # 创建第一个用户
            cur_user = 'The_First_User'
        else:
            cur_user = str(current_user.username)
        tmp = 'add_user'
        tmp += ' -c ' + cur_user
        tmp += ' -u ' + str(form.username.data)
        tmp += ' -p ' + str(form.password.data)
        tmp += ' -n ' + str(form.name.data)
        tmp += ' -m ' + str(form.email.data)
        tmp += ' -g ' + str(form.privilege.data)
        print(tmp)
        ret = com(tmp)
        # 通信
        # ret = '0'
        print(ret)
        if ret == '0':
            flash('新用户添加成功！', category='success')
            return redirect(url_for('index'))
        else:
            flash('添加失败，未登录 或 用户名已被占用 或 优先级设定错误', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('您已经登录！', category='info')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        tmp = 'login'
        tmp += ' -u ' + str(form.username.data)
        tmp += ' -p ' + str(form.password.data)
        print(tmp)
        # 通信
        ret = '0'
        ret = com(tmp)
        print(ret)
        if ret == '0':
            login_user(User(str(form.username.data)), remember=form.remember.data)
            flash('登录成功！', category='success')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('用户名不存在或密码错误', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    tmp = 'logout'
    tmp += ' -u ' + str(current_user.username)
    print(tmp)

    ret = com(tmp)

    print(ret)
    if ret == '0':
        logout_user()
        flash('您已成功登出！', category='success')
    else:
        flash('登出失败！', category='warning')
    return redirect(url_for('index'))


@app.route('/user_info', methods=['GET', 'POST'])
@login_required
def user_info():
    query_form = QueryUserForm()
    edit_form = EditUserForm()
    if edit_form.submit2.data:
        vip = 'edit_form'
    else:
        vip = 'query_form'
    if query_form.submit1.data and query_form.validate_on_submit():
        tmp = 'query_profile'
        tmp += ' -c ' + str(current_user.username)
        tmp += ' -u ' + str(query_form.username.data)
        print(tmp)
        # 通信
        ret = 'User1 Nick1 Email1@sjtu.edu.cn 10'
        ret = com(tmp)
        print(ret)
        if ret == '-1':
            flash('用户名不存在或权限不足！', category='danger')
            return redirect(url_for('user_info'))
        ret = ret.split()
        return render_template('user_info.html', query_form=query_form, info_post=ret, edit_form=edit_form,
                               vip=vip)

    if edit_form.submit2.data and edit_form.validate_on_submit():
        tmp = 'modify_profile '
        tmp += ' -c ' + str(current_user.username)
        tmp += ' -u ' + str(edit_form.username.data)
        if edit_form.password.data:
            tmp += ' -p ' + str(edit_form.password.data)
        if edit_form.name.data:
            tmp += ' -n ' + str(edit_form.name.data)
        if edit_form.email.data:
            tmp += ' -m ' + str(edit_form.email.data)
        if edit_form.privilege.data:
            tmp += ' -g ' + str(edit_form.privilege.data)
        print(tmp)
        # 通信
        ret = 'User1 Nick1 Email1@sjtu.edu.cn 10'
        ret = com(tmp)
        if ret == '-1':
            flash('修改失败！', category='warning')
        else:
            flash('修改成功！', category='success')
        return render_template('user_info.html', query_form=query_form, info_post=None, edit_form=edit_form,
                               vip=vip)

    return render_template('user_info.html', query_form=query_form, info_post=None, edit_form=edit_form, vip=vip)


@app.route('/train_info', methods=['GET', 'POST'])
def train_info():
    add_form = AddTrainForm()
    release_form = ReleaseTrainForm()
    delete_form = DeleteTrainForm()
    query_form = QueryTrainForm()

    if add_form.submit1.data and add_form.validate_on_submit():
        print(add_form.startTimes.data)
        tmp = 'add_train'
        tmp += ' -i ' + str(add_form.trainID.data)
        tmp += ' -n ' + str(add_form.stationNum.data)
        tmp += ' -m ' + str(add_form.seatNum.data)
        tmp += ' -s ' + str(add_form.stations.data).replace(' ', '|')
        tmp += ' -p ' + str(add_form.prices.data).replace(' ', '|')
        tmp += ' -x ' + str(add_form.startTimes.data)[0:5]
        tmp += ' -t ' + str(add_form.travelTimes.data).replace(' ', '|')
        tmp += ' -o ' + str(add_form.stopoverTimes.data).replace(' ', '|')
        tmp += ' -d ' + str(add_form.startSaleDate.data)[-5:] + '|' + str(add_form.endSaleDate.data)[-5:]
        tmp += ' -y ' + str(add_form.type.data)
        print(tmp)
        # 通信
        ret = '0'
        ret = com(tmp)
        print(ret)
        if ret == '0':
            flash('"' + str(add_form.trainID.data) + '"车次' + '添加成功！', category='success')
            return redirect(url_for('train_info'))
        else:
            flash('"' + str(add_form.trainID.data) + '"车次' + '添加失败！', category='warning')

    if release_form.submit2.data and release_form.validate_on_submit():
        tmp = 'release_train'
        tmp += ' -i ' + str(release_form.releaseID.data)
        print(tmp)
        # 通信
        ret = '0'
        ret = com(tmp)
        print(ret)
        if ret == '0':
            flash('"' + str(release_form.releaseID.data) + '"车次' + '发布成功！', category='success')
            return redirect(url_for('train_info'))
        else:
            flash('"' + str(release_form.releaseID.data) + '"车次' + '发布失败！', category='warning')

    if delete_form.submit3.data and delete_form.validate_on_submit():
        tmp = 'delete_train'
        tmp += ' -i ' + str(delete_form.deleteID.data)
        print(tmp)
        # 通信
        ret = '0'
        ret = com(tmp)
        if ret == '0':
            flash('"' + str(delete_form.deleteID.data) + '"车次' + '删除成功！', category='success')
            return redirect(url_for('train_info'))
        else:
            flash('"' + str(delete_form.deleteID.data) + '"车次' + '删除失败！', category='warning')

    if query_form.submit4.data and query_form.validate_on_submit():
        tmp = 'query_train'
        tmp += ' -i ' + str(query_form.QueryID.data)
        tmp += ' -d ' + str(query_form.QueryDate.data)[-5:]
        print(tmp)
        # 通信
        ret = 'HAPPY_TRAIN G\n上院 xx-xx xx:xx -> 07-01 19:19 0 1000\n中院 07-02 05:19 -> 07-02 05:24 114 1000\n下院 07-02 15:24 -> xx-xx xx:xx 628 x'
        ret = com(tmp)
        ret = ret.replace('xx-xx', '------')
        ret = ret.replace('xx:xx', '------')
        ret = ret.replace('x', '------')
        print(ret)
        if ret == '-1':
            flash('"' + str(query_form.QueryID.data) + '"车次' + '查询失败！', category='warning')
            return render_template('train_info.html', add_form=add_form, release_form=release_form,
                                   delete_form=delete_form, query_form=query_form, query_post=None)
        ret = ret.split('\n')
        for i in range(len(ret)):
            ret[i] = ret[i].split()
        print(ret)
        return render_template('train_info.html', add_form=add_form, release_form=release_form, delete_form=delete_form,
                               query_form=query_form, query_post=ret)
    return render_template('train_info.html', add_form=add_form, release_form=release_form, delete_form=delete_form,
                           query_form=query_form)


@app.route('/train_ticket', methods=['GET', 'POST'])
def train_ticket():
    query_form = QueryTicketForm()
    buy_form = BuyTicketForm()
    if query_form.submit1.data and query_form.validate_on_submit():
        tmp = str(query_form.Ways.data)
        tmp += ' -s ' + str(query_form.Dep.data)
        tmp += ' -t ' + str(query_form.Arr.data)
        tmp += ' -d ' + str(query_form.Date.data)[-5:]
        tmp += ' -p ' + str(query_form.Sort.data)
        print(tmp)
        # 通信
        ret = '1\nHAPPY_TRAIN 中院 08-17 05:24 -> 下院 08-17 15:24 514 1000'
        ret = com(tmp)
        if ret == '-1':
            flash('查询失败')
            return render_template('train_ticket.html', query_form=query_form, buy_form=buy_form)
        ret = ret.split('\n')
        for i in range(len(ret)):
            ret[i] = ret[i].split()
        print(ret)
        return render_template('train_ticket.html', query_form=query_form, query_post=ret, buy_form=buy_form)
    if buy_form.submit2.data and buy_form.validate_on_submit():
        tmp = 'buy_ticket'
        tmp += ' -u ' + str(current_user.username)
        tmp += ' -i ' + str(buy_form.ID.data)
        tmp += ' -d ' + str(buy_form.DT.data)[-5:]
        tmp += ' -n ' + str(buy_form.NM.data)
        tmp += ' -f ' + str(buy_form.ST.data)
        tmp += ' -t ' + str(buy_form.ED.data)
        tmp += ' -q ' + str(buy_form.choice.data)
        print(tmp)
        # 通信
        ret = '257000'
        ret = com(tmp)
        print(ret)
        if ret == '-1':
            flash('购票失败！', category='danger')
        elif ret == 'queue':
            flash('余票不足，您提交的购票订单已加入候补！', category='warning')
        else:
            flash(str(buy_form.ID.data) + '次列车 ' + str(buy_form.DT.data)[-5:] + ' ' + str(buy_form.ST.data) + '➡' + str(
                buy_form.ED.data) + ' 购票成功！￥ ' + ret, category='success')
    return render_template('train_ticket.html', query_form=query_form, buy_form=buy_form)


@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    tmp = 'query_order'
    tmp += ' -u ' + str(current_user.username)
    print(tmp)
    # 通信
    ret = '2\n[pending] HAPPY_TRAIN 上院 08-17 05:24 -> 下院 08-17 15:24 628 500\n[refunded] HAPPY_TRAIN 上院 08-17 05:24 -> ' \
          '下院 08-17 15:24 628 500 '
    ret = com(tmp)
    ret = ret.replace('[success]', '购票成功')
    ret = ret.replace('[pending]', '候补中')
    ret = ret.replace('[refunded]', '已退票')
    print(ret)
    ret = ret.split('\n')
    for i in range(len(ret)):
        ret[i] = ret[i].split()

    return render_template('order.html', post=ret)


@app.route('/refund/<number>', methods=['GET', 'POST'])
@login_required
def refund(number):
    tmp = 'refund_ticket'
    tmp += ' -u ' + str(current_user.username)
    tmp += ' -n ' + str(number)
    print(tmp)
    # 通信
    ret = '0'
    ret = com(tmp)
    if ret == '0':
        flash('退订成功！', category='success')
    else:
        flash('退订失败！', category='danger')
    return redirect(url_for('order'))
