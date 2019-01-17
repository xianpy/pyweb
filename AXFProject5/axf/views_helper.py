from axf.models import Cart


def total_price(request):   # 计算选中的购物车中的商品总价
    user_id = request.session.get("user_id")
    carts = Cart.objects.filter(user_id=user_id,ischoose=True)
    total = 0
    for cart in carts:
        total += cart.goods.price * cart.cart_num
    return total