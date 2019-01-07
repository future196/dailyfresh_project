from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime
from decimal import Decimal
from cart.models import Cart
from user.models import User
from order.models import Order, OrderDetail
from goods.models import Goods
from user.decorators import login_required

# Create your views here.

@login_required
def order(request, where_from):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    if where_from == "cart":
        try:
            cart_id = request.POST.getlist("checked")
            order_list = []
            for id in cart_id:
                order_list.append(Cart.objects.get(id=id))
            if user.telephone != "":
                telephone = user.telephone[:3] + "****" + user.telephone[-4:]
            else:
                telephone = ""
            context = {
                'user': user,
                'order_list': order_list,
                'order_count': len(order_list),
                'telephone': telephone,
                'type': "cart",
            }
        except:
            return redirect("/cart/")
    else:
        if user.telephone != "":
            telephone = user.telephone[:3] + "****" + user.telephone[-4:]
        else:
            telephone = ""
        count = request.POST.get("num")
        goods_id = request.POST.get("goods_id")
        context = {
            'user': user,
            'order_count': "1",
            'telephone': telephone,
            'type': "detail",
            'count': count,
            'goods': Goods.objects.get(id=goods_id),
        }

    return render(request, "order/order.html", context)

def add_order(request):
    post = request.POST
    # 保存一个事物点
    tran_id = transaction.savepoint()
    if post.get("goods_id"):
        try:
            goods_id = post.get('goods_id')
            total = post.get('total')
            address = post.get('address')
            count = post.get("count")
            order = Order()
            now = datetime.now()
            user_id = request.session.get('user_id')
            order.order_id = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)
            order.user = User.objects.get(id=user_id)
            order.date = now
            order.total = Decimal(total)
            order.address = address
            order.save()
            # 遍历购物车中提交信息，创建订单详情表
            goods = Goods.objects.get(id=goods_id)
            # 判断库存是否够
            if int(goods.stock) >= int(count):
                # 库存够，移除购买数量并保存
                goods.stock -= int(count)
                goods.save()
                # 创建订单详情表
                detail = OrderDetail()
                detail.goods_id = int(goods.id)
                detail.order_id = int(order.order_id)
                detail.price = Decimal(float(goods.price))
                detail.count = int(count)
                detail.save()
                # 循环删除购物车对象
            else:
                # 库存不够出发事务回滚
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'status': 2})
        except Exception as e:
            transaction.savepoint_rollback(tran_id)
    else:
        try:
            order_list = post.getlist('id[]')
            total = post.get('total')
            address = post.get('address')
            order = Order()
            now = datetime.now()
            user_id = request.session.get('user_id')
            order.order_id = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)
            order.user = User.objects.get(id=user_id)
            order.date = now
            order.total = Decimal(total)
            order.address = address
            order.save()
            # 遍历购物车中提交信息，创建订单详情表
            for order_id in order_list:
                cart = Cart.objects.get(id=order_id)
                goods = Goods.objects.get(id=cart.goods_id)
                # 判断库存是否够
                if int(goods.stock) >= int(cart.count):
                    # 库存够，移除购买数量并保存
                    goods.stock -= int(cart.count)
                    goods.save()
                    goods = cart.goods
                    # 创建订单详情表
                    detail = OrderDetail()
                    detail.goods_id = int(goods.id)
                    detail.order_id = int(order.order_id)
                    detail.price = Decimal(float(goods.price))
                    detail.count = int(cart.count)
                    detail.save()
                    # 循环删除购物车对象
                    cart.delete()
                    request.session['cart_count'] = request.session['cart_count'] - 1
                else:
                    # 库存不够出发事务回滚
                    transaction.savepoint_rollback(tran_id)
                    return JsonResponse({'status': 2})
        except Exception as e:
            transaction.savepoint_rollback(tran_id)
    return JsonResponse({'status': 1})

def pay(request,order_id):
    order = Order.objects.get(order_id=order_id)
    order.is_pay = 1
    order.save()
    return JsonResponse({'status': '已支付'})