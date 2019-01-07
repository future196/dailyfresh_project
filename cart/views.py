from django.shortcuts import render, HttpResponse, redirect
from cart.models import Cart
from user.models import User
from goods.models import Goods
from django.http import JsonResponse
from user.decorators import login_required

# Create your views here.


@login_required
def cart(request):
    user_id = request.session['user_id']
    carts = Cart.objects.filter(user=user_id).order_by("-id")
    context = {
        'carts': carts,
    }
    return render(request, "cart/cart.html", context)


def add_cart(request, goods_id, count):
    user_id = request.session["user_id"]
    cart_goods = Cart.objects.filter(user=user_id, goods=goods_id)
    if len(cart_goods) >= 1:
        cart_goods = cart_goods[0]
        cart_goods.count = cart_goods.count + int(count)
        cart_goods.save()
    else:
        user = User.objects.get(id=user_id)
        goods = Goods.objects.get(id=goods_id)
        cart = Cart(user=user, goods=goods, count=count)
        cart.save()

    cart_count = Cart.objects.filter(user=user_id).count()
    request.session['cart_count'] = cart_count

    context = {
        "cart_count": cart_count,
    }
    return JsonResponse(context)



def delete_cart(request, cart_id):
    Cart.objects.get(id=cart_id).delete()
    count = request.session['cart_count']
    request.session['cart_count'] = count - 1
    return redirect("/cart/")


def num_change(request, cart, type, num):
    cart = Cart.objects.get(id=cart)
    if type == "add":
        cart.count = cart.count + 1
    if type == "input":
        cart.count = num
    if type == "minus":
        if cart.count == 1:
            cart.count = cart.count - 0
        else:
            cart.count = cart.count - 1
    cart.save()
    total = cart.goods.price * int(cart.count)
    context = {
        'count': cart.count,
        'total': total,
    }
    return JsonResponse(context)
