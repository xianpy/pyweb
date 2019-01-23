from django.conf.urls import url
from django.urls import re_path,path

from axf import views

app_name = 'axf'


urlpatterns = [
    path('home/',views.home,name='home'),
    path('search/', views.search, name='search'),
    path('go_search/<childcid>/',views.go_search,name='go_search'),
    #以上刘璋豪
    path('shop/<goodid>/',views.market1,name="market1"),
    path('addcart/',views.addcart,name="addcart"),
    #以上赵靖
    path('index/', views.home, name='index'),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('wronglogin/<username>/<password>/', views.go_login_withwrong, name="wronglogin"),
    path('logout/', views.logout, name="logout"),
    path('centre/', views.Center, name='centre'),
    path('buy_goods/', views.Buy_goods, name='buy'),
    path('collect/', views.Collect, name='collect'),
    path('site/', views.Site, name='site'),
    path('delete/<id>/', views.delete_byid, name='delete'),
    path('info/', views.Info, name='info'),
    path('account/', views.Account, name='account'),
    path('bind/', views.Bind, name='bind'),
    path('purse/', views.Purse, name='purse'),
    #以上周民尉

    path('market/', views.gocart,name="market"),
    path('gocart/',views.gocart,name="gocart"),
    path('addshop/',views.addShopping),
    path('subcart/',views.subShopping),
    path('changeselect/',views.change_cart_select),
    path('changeselectall/',views.change_select_all),
    path("makeorders/",views.make_order),
    path("orderdetail/",views.order_detail),
    path("pay/",views.pay),
    url('', views.home, name='home'),
]