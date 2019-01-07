from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from user.models import User
from hashlib import sha1
from django.http import JsonResponse
from .decorators import login_required
from goods.models import Goods
from order.models import Order,OrderDetail
from cart.models import Cart
from django.core.paginator import Paginator

# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        if password1 == password2:
            hash = sha1()
            hash.update(password2.encode("utf8"))
            password = hash.hexdigest()
            user = User(name=username, password=password, email=email)
            user.save()
            return redirect("/user/login/")
    else:
        return render(request, "user/register.html")

def register_exist(request):
    username = request.GET.get('username')
    count = User.objects.filter(name=username).count()
    return JsonResponse({'count': count})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember", 0)
        user = User.objects.filter(name=username)
        if len(user) == 1:
            hash = sha1()
            hash.update(password.encode("utf8"))
            password_hash = hash.hexdigest()
            if password_hash == user[0].password:
                request.session["user_id"] = user[0].id
                request.session["username"] = user[0].name
                cart_count = Cart.objects.filter(user=user[0])
                request.session["cart_count"] = len(cart_count)
                red = HttpResponseRedirect("/goods/home/")
                if remember == 1:
                    red.set_cookie("username", username.encode('utf-8').decode('latin-1'))
                else:
                    red.set_cookie('username', '', max_age=-1)
                return red
            else:
                username = request.COOKIES.get("username", "")
                username = username.encode('latin-1').decode('utf-8')
                context = {
                    'error_name': 0, 'error_password': 1, 'username': username,
                }
                return render(request, "user/login.html", context)
        else:
            username = request.COOKIES.get("username", "")
            username = username.encode('latin-1').decode('utf-8')
            context = {
                'error_name': 1, 'error_password': 0, 'username': username,
            }
            return render(request, "user/login.html", context)
    else:
        return render(request, "user/login.html")

def logout(request):
    request.session.flush()
    return redirect('/goods/home/')


@login_required
def info(request):
    user_id = request.session.get("user_id","")
    if user_id == "":
        redirect("/user/login/")
    else:
        user = User.objects.get(id=user_id)
        recent_goods = "recent_goods_%s" % user_id
        recent = request.COOKIES.get(recent_goods, "")
        recent = recent.split(",")
        recent_list = []
        for id in recent:
            try:
                goods = Goods.objects.get(id=id)
                recent_list.append(goods)
            except:     # 如果最近浏览不存在则忽略此商品
                pass

        context = {
            'username': user.name,
            'email': user.email,
            'address': user.address,
            'recent_list': recent_list,
        }
        return render(request, "user/user_center_info.html", context)

@login_required
def order(request):
    user_id = request.session.get("user_id")
    order = Order.objects.filter(user_id=user_id).order_by("-date")
    context = {
        'orders': order,
    }
    return render(request, "user/user_center_order.html",context)

def site(request):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        receive_user = request.POST.get("receive_user")
        address = request.POST.get("address")
        telephone = request.POST.get("telephone")
        zip_code = request.POST.get("zip_code")
        user = User.objects.get(id=user_id)
        user.telephone = telephone
        user.zip_code = zip_code
        user.address = address
        user.receive_user = receive_user
        user.save()
        return redirect("/user/site/")
    else:
        user = User.objects.get(id=user_id)
        context = {
            'user': user,
            'telephone': user.telephone[:3]+"****"+user.telephone[-4:],
        }
        return render(request, "user/user_center_site.html", context)