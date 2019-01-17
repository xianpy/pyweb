from django.conf.urls import url
from django.urls import re_path,path

from axf import views

app_name = 'axf'


urlpatterns = [
    url('home/',views.home,name='home'),
    path('market/', views.market,name="market"),
    path('market1/<foodtypeid>/<childtypeid>/<sortcode>/',views.market1,name="market1"),
    path('mine/',views.mine,name="mine"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('gocart/',views.gocart,name="gocart"),
    path('addshop/',views.addShopping),
    path('subcart/',views.subShopping),
    path('changeselect/',views.change_cart_select),
    path('changeselectall/',views.change_select_all),
    path("makeorders/",views.make_order),
    path("orderdetail/",views.order_detail),
    path("pay/",views.pay),
]