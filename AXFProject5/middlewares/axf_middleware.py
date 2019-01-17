from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from axf.models import User

LOGIN_REQUIRED_JSON = ["/addshop/","/subcart/","/makeorders/","/gocart/","/pay/",]
LOGIN_REQUIRED = ["/orderdetail/",]


class LoginMiddleware(MiddlewareMixin):

    def process_request(self,request):  # 接收到请求时，会自动调用该方法
        print("request.path=",request.path)
        if request.path in LOGIN_REQUIRED_JSON:
            user_id = request.session.get("user_id")
            if user_id:    # 判断是否登录
                user = User.objects.get(pk=user_id)
                request.user = user   #  将当前用户对象设置到request的user属性中
            else:
                #return JsonResponse({"status":"900"})
                return redirect(reverse("axf:login"))

        if request.path in LOGIN_REQUIRED:
            user_id = request.session.get("user_id")
            if user_id:    # 判断是否登录
                user = User.objects.get(pk=user_id)
                request.user = user   #  将当前用户对象设置到request的user属性中
            else:
                return redirect(reverse("axf:login"))