
from django.http import JsonResponse
from django.shortcuts import render

from axf.models import *
from axf.views_helper import total_price
#商品详情页面
def market1(request,goodid):

    goods=Goods.objects.get(productid=goodid)
    img=goods.productimg
    price=goods.price
    name=goods.productname
    ku =goods.productnum
    allimg=goods.productlongname.split("http")[-4:-1]
    index=Goods.objects.all()
    import random
    goods1=random.choice(index)
    goods2 = random.choice(index)
    goods3 = random.choice(index)
    goodsall=[goods1,goods2,goods3]


    childids=goods.childcid
    goods_tuijian= Goods.objects.filter(childcid=childids).exclude(productid=goods.productid).order_by('-productnum')[:3]


    #将商品信息添加到历史浏览记录里
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    print(ip)
    goods_history = []
    if request.session.get(ip,False):
        print(request.session[ip])
        for i in request.session[ip].split(','):
            good1_history = Goods.objects.get(productid=int(i))
            #print(good1_history)

            goods_history.append(good1_history)
        request.session[ip]=request.session[ip]+','+goods.productid
        goods_history=goods_history[-6:][::-1]
    else:

        request.session[ip] = goods.productid

        goods_history=[]
    #详情大图的数据请求和数据解析
    url='http://product.dangdang.com/index.php?r=callback/detail&productId=%s&templateType=mall&describeMap=&shopId=8542&categoryPath=58.32.20.16.03.00'%goodid
    import requests
    resp=requests.request('post',url=url)
    print(resp,"请求")
    content_type = resp.headers.get('content-type')
    print(content_type)
    resp=resp.text

    from lxml import etree
    html=etree.HTML(resp)
    introduce_img=html.xpath("//img/@data-original")

    return render(request, 'axf/shop.html', locals())
    leftSlider = Foodtypes.objects.all()
    if childtypeid == '0':
        productList = Goods.objects.filter(categoryid=foodtypeid)
    else:
        productList = Goods.objects.filter(categoryid=foodtypeid,childcid=childtypeid)

    if sortcode == "1":
        productList = productList.order_by("-productnum")
    elif sortcode == "2":
        productList = productList.order_by("price")
    elif sortcode == "3":
        productList = productList.order_by("-price")

    user_id = request.session.get("user_id")
    if user_id:   # 如果已登录
        for product in productList:  # 遍历当前显示在闪送页面上的商品
            carts = Cart.objects.filter(user_id=user_id,goods_id=product.id)
            if carts.exists():
                cart = carts.first()
                product.cart_num = cart.cart_num
            else:
                product.cart_num = 0

    child_dict = {}  # 用来收集小类信息
    foodtype  = Foodtypes.objects.get(typeid=foodtypeid)
    childnames = foodtype.childtypenames
    childlist =  childnames.split("#") # 使用"#"拆分当前大类对应的子类信息
    for child in childlist:
        temp = child.split(":")
        child_dict[temp[0]] = temp[1]  # 封装当前大类对应的子类信息

    return render(request,'axf/market.html',locals())



def addcart(request):
    user_id = request.session.get("user_id",False)  # 从session中取出user_id
    print(user_id,"EEEEEEEEEEEEEEE")
    if user_id:
        goods_id = request.GET.get("productid")  # 接收Ajax请求传送的goods_id参数
        data = {
            'status': "200",
        }
        user=User.objects.get(id=user_id)
        request.user=user
        print(request.user)
        print(goods_id)
        goods=Goods.objects.get(productid=goods_id)
        goods_id=goods.id
        carts = Cart.objects.filter(goods_id=goods_id, user=request.user)
        print(carts)
        if carts.exists():  # 如果当前用户在购物车中已经放入了该商品
            cart = carts.first()
            cart.cart_num = cart.cart_num + int(request.GET.get("goodsnum"))  # 在原来购物车商品数上加一
            cart.save()  # 更新购物车
        else:
            goodsnum=int(request.GET.get("goodsnum"))
            cart = Cart.objects.create(goods_id=goods_id, user=request.user, cart_num=goodsnum)
        #totalPrice = total_price(request)  # 计算总价
        #data["totalPrice"] = totalPrice
        data["cart_num"] = cart.cart_num
        data['msg'] = "已经加入购物车！"
    else:
        data = {
            'status': "200",
        }
        data['msg']="请先登陆！"
    return JsonResponse(data)