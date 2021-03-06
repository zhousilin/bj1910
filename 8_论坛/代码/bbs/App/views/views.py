# -*- coding: utf-8 -*-
# @File    : views.py
# 描述     ：
# @Time    : 2020/1/7 14:33
# @Author  : 
# @QQ      :  

from flask import Blueprint, render_template
from sqlalchemy import func

from App.models import Category, db, User

bbs = Blueprint('bbs',__name__)

@bbs.route('/')
@bbs.route("/<int:cid>/")
def index(cid=0):
    """
    :param cid: 缺省是0，展示所有版块信息，否则展示指定版块信息
    :return:
    """
    # 查询大板块数据
    big_category = Category.query.filter(Category.parentid==0).all()
    small_category = Category.query.filter(Category.parentid != 0).all()

    #统计帖子数，回复数
    counts = db.session.query(func.sum(Category.replycount),func.sum(Category.forumcount)).group_by(Category.parentid).having(Category.parentid==0).all()
    print(counts[0][0],counts[0][1])
    replycount = counts[0][0]
    forumcount = counts[0][1]

    # 会员数
    user_count = User.query.count()
    print(user_count)

    new_user = User.query.order_by(-User.id).limit(1).first()
    print(new_user)

    # forumcount = Category.query(func.sum(Category.forumcount)).scalar()
    # 指定大板块
    if cid != 0:
        for big in big_category:
            if big.cid == cid:
                the_big = big
                break
        return render_template("index/index.html",**locals())
    else:
        return render_template("index/index.html", **locals())


@bbs.route("/list/<int:cid>/")
def list_category(cid):
    print(cid,type(cid))
    return "帖子列表"