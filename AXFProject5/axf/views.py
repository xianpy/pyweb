import time
import hashlib

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from axf.constants import ORDER_STATE_PAIED
from axf.models import *
from axf.views_helper import total_price

# 主页视图函数
def home(request):
    return render(request, 'axf/index.html', locals())
    wheelsList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()
    shops = Shop.objects.all()
    shop1 = shops[0]
    shop2 = shops[1:3]
    shop3 = shops[3:7]
    shop4 = shops[7:11]
    mainList = Mainshow.objects.all()
    return render(request,'axf/home.html',locals())

# 闪购超市视图函数
# categoryid参数代表大种类标识；cid代表小种类标识，sortcode代表排序码
def  market(request):

    return render(request,'axf/cart.html',locals())
def market1(request,foodtypeid,childtypeid,sortcode):
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


def mine(request):
    return render(request, 'axf/mine.html', locals())
    user_id = request.session.get("user_id")  # 从session中取出user_id
    if user_id:
        user = User.objects.get(pk=user_id)
        username = user.username
        figure_path = "uploads/" + user.icon.name
        # 未支付订单数量
        order_nopay_count = Orders.objects.filter(user_id=user_id,orderstate=ORDER_STATE_NO_PAY).count()
        # 已经支付，但未收货
        order_noreceive_count = Orders.objects.filter(user_id=user_id,orderstate=ORDER_STATE_PAIED).count()
    else:
        username = "点击登录"
    return render(request,'axf/mine.html',locals())


def register(request):
    return render(request, 'axf/register.html')
    if request.method == "GET":
        return render(request,'axf/register.html')
    elif request.method == "POST":
        userAccount = request.POST.get("userAccount")  # 接收提交的POST数据
        userPass = request.POST.get("userPass")
        userPhone = request.POST.get("userPhone")
        userAddress = request.POST.get("userAddress")
        userImg = request.FILES.get("userImg")  # 接收二进制图片
        print("userImg.name=",userImg.name)
        userImg.name = str(int(time.time()*10000)) + userImg.name  # 重新设定图片名称
        new_user = User()
        new_user.username = userAccount
        md5 = hashlib.md5()
        md5.update(userPass.encode("utf-8"))
        new_user.password = md5.hexdigest()
        new_user.tel = userPhone
        new_user.address = userAddress
        new_user.icon = userImg  # 将图片对象与用户对象关联
        new_user.save()
        return redirect(reverse("axf:login"))


def login(request):   # 登录
    if request.method == "GET":
        return render(request,'axf/login.html')
    elif request.method == "POST":
        loginname = request.POST.get("loginname")
        loginpwd = request.POST.get("loginpwd")
        md5 = hashlib.md5()
        md5.update(loginpwd.encode("utf-8"))
        loginpwd = md5.hexdigest()
        users = User.objects.filter(username=loginname,password=loginpwd)
        if users:
            user = users.first()
            request.session["user_id"] = user.id  # 登录成功后，设置session属性

            return redirect(reverse("axf:mine"))
        else:
            return redirect(reverse("axf:login"))


def logout(request):
    request.session.flush()
    return redirect(reverse("axf:mine"))

# 进入购物车
def gocart(request):
    return render(request, 'axf/cart.html', locals())
    carts = Cart.objects.filter(user=request.user)
    select_all_flag = not Cart.objects.filter(user=request.user,ischoose=False).exists() # 是否全部选中购物车记录，若购物车全选，则返回True
    totalPrice = total_price(request)  # 计算总价
    return render(request,'axf/cart.html',locals())

# 在购物车中加
def addShopping(request):   # 添加到购物车
    goods_id = request.GET.get("goods_id")   # 接收Ajax请求传送的goods_id参数
    data = {
        'status':"200",
    }
    carts = Cart.objects.filter(goods_id=goods_id,user=request.user)
    if carts.exists():   # 如果当前用户在购物车中已经放入了该商品
        cart = carts.first()
        cart.cart_num = cart.cart_num + 1   # 在原来购物车商品数上加一
        cart.save()  # 更新购物车
    else:
        cart = Cart.objects.create(goods_id=goods_id,user=request.user,cart_num=1)
    totalPrice = total_price(request)  # 计算总价
    data["totalPrice"] = totalPrice
    data["cart_num"] = cart.cart_num
    return JsonResponse(data)


# 从购物车中减
def subShopping(request):
    goods_id = request.GET.get("goods_id")  # 接收Ajax请求传送的goods_id参数
    data = {
        'status': "200",
    }
    carts = Cart.objects.filter(goods_id=goods_id,user=request.user)   # 查询当前用户放入购物车中的指定商品
    if carts.exists():   # 如果当前用户在购物车中已经放入了该商品
        cart = carts.first()
        cart.cart_num = cart.cart_num - 1
        if cart.cart_num == 0:   # 如果减1后，当前用户的购物车中该商品数量为0，则删除该购物车记录
            data["cart_num"] = 0
            cart.delete()
        else:
            cart.save()
            data["cart_num"] = cart.cart_num
        totalPrice = total_price(request)  # 计算总价
        data["totalPrice"] = totalPrice
    else:  # 购物车中本来就无此商品
        data["status"] = "901"
        data["msg"] = "购物车中无此商品，不能减！"

    return JsonResponse(data)

def change_cart_select(request):   # 点击某个购物车选中状态
    cartid = request.GET.get("cartid")
    cart = Cart.objects.get(pk=cartid)  # 根据购物车主键查询购物车
    cart.ischoose = not cart.ischoose   # 选中状态取反
    cart.save()  # 更新购物车选中状态到数据库

    totalPrice = total_price(request)   # 计算总价

    user_id = request.session.get("user_id")
    select_all_flag = not Cart.objects.filter(user_id=user_id,ischoose=False).exists() # 是否全部选中购物车记录，若购物车全选，则返回True
    data = {
        "ischoose":cart.ischoose,
        "select_all_flag":select_all_flag,
        "totalPrice":totalPrice,
    }
    return JsonResponse(data)

def change_select_all(request):   # 改变全选状态
    is_select = request.GET.get("hope_status")  # 接收全选span希望的状态
    print("is_select=",is_select)
    user_id = request.session.get("user_id")
    carts = Cart.objects.filter(user_id=user_id)   # 获取当前用户的购物车记录
    if is_select == "true":
        for cart in carts:
            cart.ischoose = True
            cart.save()
    else:
        for cart in carts:
            cart.ischoose = False
            cart.save()

    totalPrice = total_price(request)  # 计算总价

    data = {
        "is_select":is_select,
        "totalPrice":totalPrice,
    }
    return JsonResponse(data)

def make_order(request):    # 创建订单
    carts = Cart.objects.filter(user=request.user,ischoose=True) # 查询登录用户选中的购物车记录
    orders = Orders()  # 创建订单对象
    orders.user = request.user
    orders.totalPrice = total_price(request)
    orders.save()  # 保存订单
    for cart in carts:
        order_goods = OrderGoods()   # 创建订单商品对象
        order_goods.orders = orders  # 关联订单对象
        order_goods.goods = cart.goods  # 关联商品
        order_goods.goods_num = cart.cart_num # 设置订单商品数量
        order_goods.save()  # 保存订单商品
        cart.delete()  # 删除购物车记录

    data = {
        "status":"200",
        "orderid":orders.id,
    }
    return JsonResponse(data)

def order_detail(request):
    order_id = request.GET.get("order_id")   # 接收传递的新建订单id
    order = Orders.objects.filter(id=order_id,user=request.user).first()
    return render(request,'axf/order_detail.html',locals())

def pay(request):
    order_id = request.GET.get("order_id")  # 接收付款订单id
    order = Orders.objects.get(pk=order_id)
    order.orderstate = ORDER_STATE_PAIED   # 更改状态为已支付
    order.save()
    data = {
        "status":"200",
        "msg":"支付成功！"
    }
    return JsonResponse(data)






