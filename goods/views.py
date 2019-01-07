from django.shortcuts import render, HttpResponse
from goods.models import Type, Goods
from django.core.paginator import Paginator
from django.core.cache import cache
# import redis
# # pool = redis.ConnectionPool(host="127.0.0.1", port="6379")
# cache = redis.Redis(host="127.0.0.1", port="6379")
# Create your views here.

def home(request):
    type_fruits = Type.objects.filter(name='fruits')

    type_aquaculture = Type.objects.filter(name='aquaculture')
    type_meat = Type.objects.filter(name='meat')
    type_eggs = Type.objects.filter(name='eggs')
    type_vegetables = Type.objects.filter(name='vegetables')
    type_frozen = Type.objects.filter(name='frozen')

    goods_fruits = Goods.objects.filter(type=type_fruits[0]).order_by("-id")[:4]
    goods_aquaculture = Goods.objects.filter(type=type_aquaculture[0]).order_by("-id")[:4]
    goods_meat = Goods.objects.filter(type=type_meat[0]).order_by("-id")[:4]
    goods_eggs = Goods.objects.filter(type=type_eggs[0]).order_by("-id")[:4]
    goods_vegetables = Goods.objects.filter(type=type_vegetables[0]).order_by("-id")[:4]
    goods_frozen = Goods.objects.filter(type=type_frozen[0]).order_by("-id")[:4]

    goods_fruits_hits = Goods.objects.filter(type=type_fruits[0]).order_by("-hits")[:4]
    goods_aquaculture_hits = Goods.objects.filter(type=type_aquaculture[0]).order_by("-hits")[:4]
    goods_meat_hits = Goods.objects.filter(type=type_meat[0]).order_by("-hits")[:4]
    goods_eggs_hits = Goods.objects.filter(type=type_eggs[0]).order_by("-hits")[:4]
    goods_vegetables_hits = Goods.objects.filter(type=type_vegetables[0]).order_by("-hits")[:4]
    goods_frozen_hits = Goods.objects.filter(type=type_frozen[0]).order_by("-hits")[:4]
    # if cache.get("xuwei") is None:
    #     cache.set("xuwei", goods_fruits, 5)
    #     print("数据库查询")
    # else:
    #     print("使用缓存")
    context = {
        # "goods_fruits": cache.get("xuwei"),
        "goods_fruits": goods_fruits,
        "goods_aquaculture": goods_aquaculture,
        "goods_meat": goods_meat,
        "goods_eggs": goods_eggs,
        "goods_vegetables": goods_vegetables,
        "goods_frozen": goods_frozen,

        "goods_fruits_hits": goods_fruits_hits,
        "goods_aquaculture_hits": goods_aquaculture_hits,
        "goods_meat_hits": goods_meat_hits,
        "goods_eggs_hits": goods_eggs_hits,
        "goods_vegetables_hits": goods_vegetables_hits,
        "goods_frozen_hits": goods_frozen_hits,

        'home': "is", # 传什么数值不重要，有数值判断存在就行
    }
    return render(request, "goods/home.html", context)


def goods_list(request, type, sort, page):
    newest_goods = Goods.objects.all().order_by("-id")[:2]
    type = Type.objects.filter(name=type)[0]
    if sort == "date":
        goods = Goods.objects.filter(type=type).order_by('-id')
    elif sort == "price":
        goods = Goods.objects.filter(type=type).order_by('price')
    elif sort == "hits":
        goods = Goods.objects.filter(type=type).order_by('-hits')

    paginator = Paginator(goods, 10)  # 使用分页器把所有商品分为每页10个
    goods = paginator.page(page)    # 取某页的所有商品
    pages = paginator.page_range  # 获取总页数
    context = {
        'newest_goods': newest_goods,
        'goods': goods,
        'sort': sort,
        'list': '1',
        'title': type.title,
        'pages': pages,
        'page_current': int(page),
        'type': type.name,
        'page_length': len(pages)
    }
    return render(request, "goods/list.html", context)



def detail(request, type, goods_id):
    newest_goods = Goods.objects.all().order_by("id")[:2]
    type = Type.objects.filter(name=type)[0]
    goods = Goods.objects.get(id=goods_id)
    goods.hits = goods.hits + 1     # 增加点击量
    goods.save()
    context = {
        'newest_goods': newest_goods,
        'detail': '1',
        'title': type.title,
        'type': type.name,
        'goods': goods,
    }
    ren = render(request, "goods/detail.html", context)
    recent_goods = "recent_goods_%s" % request.session.get("user_id")
    recent = request.COOKIES.get(recent_goods, "none")
    if recent != "none":
        goods_ids = recent.split(",")
        if goods_ids.count(goods_id) >= 1:
            goods_ids.remove(goods_id)
        goods_ids.insert(0, goods_id)
        if len(goods_ids) >= 6:
            del goods_ids[5]
        recent = ",".join(goods_ids)
        ren.set_cookie(recent_goods, recent)
        ren.set_cookie("add_cart", "detail")
        return ren
    else:
        recent = str(goods_id)
        ren.set_cookie(recent_goods, recent)
    return ren

def search(request):
    key_code = request.POST.get("key_code")
    goods = Goods.objects.filter(name__contains=key_code)
    context = {
        'goods': goods,
        'list': '1',
        'search': 1,
    }
    return render(request, "goods/search_list.html", context)

