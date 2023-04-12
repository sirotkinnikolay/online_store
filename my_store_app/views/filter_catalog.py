from .base import *
from django.shortcuts import render
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *


class FilterCatalogView(View):
    """Фильтрация товаров по ценовому диапазону, названию,
     наличию и бесплатной доставке"""

    def get(self, request):
        result = base(request)
        old_filter = UserCatalogFilter.objects.get(user_filter=request.COOKIES.get('csrftoken'))
        return render(request, 'catalog.html', {'products': filter_result_objects(old_filter.variable),
                                                'tags': tags_list(), 'categories': result[0],
                                                'basket_product_count': result[2], 'total': result[3],
                                                'avatar': avatar(request)})

    def post(self, request):
        result = base(request)
        if len(UserCatalogFilter.objects.filter(user_filter=request.COOKIES.get('csrftoken'))) == 0:
            UserCatalogFilter.objects.create(user_filter=request.COOKIES.get('csrftoken'), variable=request.POST)
        else:
            new_filter = UserCatalogFilter.objects.get(user_filter=request.COOKIES.get('csrftoken'))
            new_filter.variable = request.POST
            new_filter.save()

        return render(request, 'catalog.html', {'products': filter_result_objects(request.POST), 'tags': tags_list(),
                                                'categories': result[0], 'basket_product_count': result[2],
                                                'total': result[3], 'avatar': avatar(request)})
