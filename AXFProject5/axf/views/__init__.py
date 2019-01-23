import time
import hashlib
from axf.views.shouye_liuzhanghao import *
from axf.views.xiangqing_zhaojing import *
from axf.views.mine_zhouminwen import *
from axf.views.shoppingcar_zuotianhao import *
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from axf.constants import ORDER_STATE_PAIED
from axf.models import *
#from axf.views_helper import total_price

# 主页视图函数,刘璋豪
def home1(request):
    pass
# 购物车视图函数，左田浩
# categoryid参数代表大种类标识；cid代表小种类标识，sortcode代表排序码
def  market(request):
    pass
    return render(request,'axf/cart.html',locals())



#商品详情页面 ,赵靖
def market2(request,goodid):
    pass



#加入购物车，赵靖
def addcart1(request):
    pass

#会员中心，周民尉
def mine1(request):
    pass

def register1(request):
    pass


def login1(request):   # 登录
    pass


def logout1(request):
    pass

# 进入购物车
def gocart1(request):
    pass







