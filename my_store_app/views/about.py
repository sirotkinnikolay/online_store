from .base import *
from django.shortcuts import render
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *


class AboutView(View):
    """Страница информации о магазине"""

    def get(self, request):
        result = base(request)
        try:
            product_0 = Product.objects.select_related('category').select_related('shop').all()[0]
            product_1 = Product.objects.select_related('category').select_related('shop').all()[1]
        except IndexError:
            return render(request, 'about.html',
                          {'categories': result[0], 'basket_product_count': result[2]})
        return render(request, 'about.html', {'product_0': product_0, 'product_1': product_1, 'categories': result[0],
                                              'basket_product_count': result[2], 'total': result[3],
                                              'avatar': avatar(request)})
