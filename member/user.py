# -*- coding=utf-8 -*-

from flask import request,session,render_template,\
                  redirect, url_for

from .member_app import member_app
from models import User
from libs import db
import json
from forms.account_form import EditInfoForm

# 用户信息修改
@member_app.route("/user/edit", methods=['get', 'post'])
def userEdit():
    # 普通会员只能修改自己的资料
    # 修改资料的时候还需要验证密码
    form =EditInfoForm()
    user = User.query.filter_by(username=session['user']).one()
    if form.validate_on_submit():

        user.realname = form.data['name']
        user.sex = form.data['sex']
        user.mylike = "|".join(form.data['like'])
        user.city = form.data['city']
        user.intro = form.data['intro']
        try:
            db.session.commit()
        except Exception as e:
            print(e)
    elif form.errors:
        print(form.errors)
    else:
        form.name.data = user.realname
        form.sex.data = user.sex
        form.like.data = user.mylike.split("|")
        form.city.data = user.city
        form.intro.data = user.intro
    return render_template("member/info/info_edit.html", user=user, form=form)
