from django.shortcuts import render
from axf.models import *


def search(request):
    keywords = request.GET.get('search')
    profuctList = Goods.objects.filter(childcidname__contains=keywords)
    return render(request, 'axf/search.html', locals())


def go_search(request, childcid):
    profuctList = Goods.objects.filter(childcid=childcid)
    return render(request, 'axf/search1.html', locals())


# 主页视图函数
def home(request):
    wheelsList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()[:2]
    shops = Shop.objects.all()
    shop1 = shops[0]
    shop2 = shops[1:3]
    shop3 = shops[3:7]
    shop4 = shops[7:11]
    mainList = Mainshow.objects.all()
    # 分类导航栏
    leftSlider = Foodtypes.objects.all()
    goods = Goods.objects.all()
    productList1 = Goods.objects.filter(categoryid='4005625')[:6]
    productList2 = Goods.objects.filter(categoryid='4010991')[:6]
    productList3 = Goods.objects.filter(categoryid='4010984')[:6]
    productList4 = Goods.objects.filter(categoryid='4005627')[:6]
    cart_goods = Cart.objects.all()
    return render(request, 'axf/index.html', locals())