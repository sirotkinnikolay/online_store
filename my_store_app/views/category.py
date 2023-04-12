from .base import *
from django.shortcuts import render
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *


class CategoryView(View):
    """Формирование списка категорий, популярных товаров,
     лимитированных, баннеров и путей до изображений этих категорий (index.html), главная страница"""

    def get(self, request):
        result = base(request)
        popular_product = Product.objects.select_related('category').select_related('shop').all().order_by('-reviews')[
                          :8]
        limited_offer = Product.objects.filter(limited_offer=True)[:1]
        limited_offer_date = str(limited_offer[0].limited_offer_date.strftime("%d.%m.%Y %H:%M"))
        try:
            discount_price = round(limited_offer[0].price / 100 * (100 - limited_offer[0].discount))
        except ZeroDivisionError:
            discount_price = limited_offer[0].price
        except IndexError:
            discount_price = 0
        banners = Product.objects.select_related('category').select_related('shop').all().order_by('-rating')[:4]
        limited_edition = Product.objects.filter(limited_edition=True)

        return render(request, 'index.html', {'categories': result[0],
                                              'popular_product': popular_product,
                                              'limited_offer': limited_offer,
                                              'banners': banners,
                                              'limited_edition': limited_edition,
                                              'limited_offer_date': limited_offer_date,
                                              'discount_price': discount_price,
                                              'basket_product_count': result[2],
                                              'total': result[3],
                                              'avatar': avatar(request)})
