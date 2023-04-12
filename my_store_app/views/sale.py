from .base import *
from django.shortcuts import render
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
import datetime


class SaleView(View):
    """Страница распродажи товаров"""

    def get(self, request):
        result = base(request)
        sal_products = Sales.objects.select_related('product').select_related('shop').all()
        for limit in sal_products:
            if limit.dateTo < datetime.datetime.now().date():
                Sales.objects.filter(id=limit.id).delete()
        return render(request, 'sale.html', {'sal_products': sal_products, 'categories': result[0],
                                             'basket_product_count': result[2], 'total': result[3],
                                             'avatar': avatar(request)})
