
from django.http import JsonResponse
from django.shortcuts import render, redirect

from axf.constants import ORDER_STATE_PAIED
from axf.models import *
from axf.views_helper import total_price

# 进入购物车
def gocart(request):
    user_id=request.session.get("user_id")
    if user_id:
        carts = Cart.objects.filter(user_id=user_id)
        user=User.objects.get(id=user_id)

        select_all_flag = not Cart.objects.filter(user_id=1, ischoose=False).exists()  # 是否全部选中购物车记录，若购物车全选，则返回True
        #totalPrice = total_price(request)  # 计算总价
        return render(request, 'axf/cart.html', locals())
    else:
        return redirect('axf:login')

# 在购物车中加
def addShopping(request):  # 添加到购物车
    goods_id = request.Get.get("c_id")  # 接收Ajax请求传送的goods_id参数

    data = {
        'status': "200",
    }
    carts = Cart.objects.filter(goods_id=goods_id)
    if carts.exists():  # 如果当前用户在购物车中已经放入了该商品
        cart = carts.first()
        cart.cart_num = cart.cart_num + 1  # 在原来购物车商品数上加一
        cart.save()  # 更新购物车
    else:
        cart = Cart.objects.create(goods_id=goods_id, cart_num=1)
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
    carts = Cart.objects.filter(goods_id=goods_id, user=request.user)  # 查询当前用户放入购物车中的指定商品
    if carts.exists():  # 如果当前用户在购物车中已经放入了该商品
        cart = carts.first()
        cart.cart_num = cart.cart_num - 1
        if cart.cart_num == 0:  # 如果减1后，当前用户的购物车中该商品数量为0，则删除该购物车记录
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


def change_cart_select(request):  # 点击某个购物车选中状态
    cartid = request.GET.get("cartid")
    cart = Cart.objects.get(pk=cartid)  # 根据购物车主键查询购物车
    cart.ischoose = not cart.ischoose  # 选中状态取反
    cart.save()  # 更新购物车选中状态到数据库

    totalPrice = total_price(request)  # 计算总价

    user_id = request.session.get("user_id")
    select_all_flag = not Cart.objects.filter(user_id=user_id, ischoose=False).exists()  # 是否全部选中购物车记录，若购物车全选，则返回True
    data = {
        "ischoose": cart.ischoose,
        "select_all_flag": select_all_flag,
        "totalPrice": totalPrice,
    }
    return JsonResponse(data)


def change_select_all(request):  # 改变全选状态
    is_select = request.GET.get("hope_status")  # 接收全选span希望的状态
    print("is_select=", is_select)
    user_id = request.session.get("user_id")
    carts = Cart.objects.filter(user_id=user_id)  # 获取当前用户的购物车记录
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
        "is_select": is_select,
        "totalPrice": totalPrice,
    }
    return JsonResponse(data)


def make_order(request):  # 创建订单
    carts = Cart.objects.filter(user=request.user, ischoose=True)  # 查询登录用户选中的购物车记录
    orders = Orders()  # 创建订单对象
    orders.user = request.user
    orders.totalPrice = total_price(request)
    orders.save()  # 保存订单
    for cart in carts:
        order_goods = OrderGoods()  # 创建订单商品对象
        order_goods.orders = orders  # 关联订单对象
        order_goods.goods = cart.goods  # 关联商品
        order_goods.goods_num = cart.cart_num  # 设置订单商品数量
        order_goods.save()  # 保存订单商品
        cart.delete()  # 删除购物车记录

    data = {
        "status": "200",
        "orderid": orders.id,
    }
    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get("order_id")  # 接收传递的新建订单id
    order = Orders.objects.filter(id=order_id, user=request.user).first()
    return render(request, 'axf/order_detail.html', locals())


def pay(request):
    order_id = request.GET.get("order_id")  # 接收付款订单id
    order = Orders.objects.get(pk=order_id)
    order.orderstate = ORDER_STATE_PAIED  # 更改状态为已支付
    order.save()
    data = {
        "status": "200",
        "msg": "支付成功！"
    }
    return JsonResponse(data)

