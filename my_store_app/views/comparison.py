from .base import *
from django.shortcuts import render
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError


class ComparisonView(View):
    """Страница сравнения товаров, удаление товара из сравнения"""

    def get(self, request):
        try:
            if request.GET['q']:
                Comparison.objects.get(username=request.COOKIES.get('csrftoken'), product_id=request.GET['q']).delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except MultiValueDictKeyError:
            result = base(request)
            comparison = Comparison.objects.filter(username=request.COOKIES.get('csrftoken'))
            specif_list = []
            prod_list = []
            for i in comparison:
                prod_list.append(i.product)
                specif_list.append(Specifications.objects.filter(specifications_id=i.product.id))

            total_ifo = zip(prod_list, specif_list)

            return render(request, 'comparison.html', {'categories': result[0], 'basket_product_count': result[2],
                                                       'total': result[3], 'total_ifo': total_ifo,
                                                       'avatar': avatar(request)})


class AddComparisonView(View):
    """Добавление товара в сравнение"""

    def get(self, request):
        if len(Comparison.objects.filter(product_id=request.GET['q'])) != 1:
            if len(Comparison.objects.filter(username=request.COOKIES.get('csrftoken'))) != 2:
                Comparison.objects.create(username=request.COOKIES.get('csrftoken'), product_id=request.GET['q'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
