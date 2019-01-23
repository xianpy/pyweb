
import hashlib

from django.shortcuts import render, redirect
from django.urls import reverse

from axf.models import *


# 返回index 页面
def My_mian(request):
    return render(request,'axf/index.html')


def Center(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(pk = user_id)
        username = user.username
        return render(request,'axf/mine/base.html',locals())
    else:
        return render(request,'axf/login.html')


def Buy_goods(request):
    return render(request,'axf/mine/Buy_the_goods.html')


def Collect(request):
    return render(request,'axf/mine/collect.html')


def Site(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(pk=user_id)
        userid = user.id
        if request.method == 'GET':
            addres = user.shippingaddress_set.all()
            return render(request,'axf/mine/site.html',locals())
        elif request.method == 'POST':
            linkman = request.POST.get('linkman')
            area = request.POST.get('area')
            address = request.POST.get('address')
            postal = request.POST.get('postal')
            phone = request.POST.get('phone')
            telephone = request.POST.get('telephone')
            remark = request.POST.get('remark')

            addre = ShippingAddress.objects.create(linkman=linkman,area=area,address=address,postal=postal,phone=phone,telephone=telephone,remark=remark,shiadd_id=userid)
            return redirect(reverse('axf:site'))


def delete_byid(request,id):
    addres = ShippingAddress.objects.filter(pk=id)
    addres.delete()
    return redirect(reverse('axf:site'))


def Info(request):
    return render(request,'axf/mine/info.html')


def Account(request):
    return render(request,'axf/mine/account.html')


def Bind(request):
    return render(request,'axf/mine/bind.html')


def Purse(request):
    return render(request,'axf/mine/purse.html')



def register(request):
    if request.method == 'GET':
        return render(request,'axf/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tel = request.POST.get('phone_num')

        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()

        user = User.objects.create(username=username,password=password,tel=tel)
        return redirect(reverse('axf:login'))


def login(request):
    if request.method == 'GET':
        return render(request,'axf/login.html')
    elif request.method == 'POST':
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_userpass')

        md5 = hashlib.md5()
        md5.update(login_password.encode('utf-8'))
        login_password = md5.hexdigest()

        users = User.objects.filter(username=login_username,password=login_password)
        if users:
            user = users.first()
            request.session['user_id'] = user.id
            return redirect(reverse('axf:index'))
        else:
            return redirect(reverse("axf:wronglogin",kwargs={'username':login_username,'password':login_password}))


def go_login_withwrong(request,username,password):
    msg = "用户名或密码错误，请重新输入"
    return render(request, 'axf/login.html',locals())


def logout(request):
    request.session.flush()
    return redirect(reverse("axf:index"))
