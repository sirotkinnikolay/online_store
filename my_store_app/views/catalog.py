from .base import *
from django.shortcuts import render
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.utils.datastructures import MultiValueDictKeyError
import re


class CatalogView(View):
    """Вывод каталога товаров и функция упорядочивания вывода,
     фильтрация по переходу с выбора категории товаров в главном меню"""

    def get(self, request):
        result = base(request)
        try:
            sort_flag = request.GET['q']
        except MultiValueDictKeyError:
            sort_flag = None

        try:
            if request.GET['q'].split('-')[1] == 'sort':
                products = Product.objects.filter(category_id=request.GET['q'].split('-')[0])
            elif request.GET['q'].split('-')[1] == 'tag':
                products = Product.objects.filter(tags__tags_name=sort_flag.split('-')[0])
            else:
                products = Product.objects.all()

            return render(request, 'catalog.html',
                          {'products': products, 'tags': tags_list(), 'categories': result[0],
                           'basket_product_count': result[2], 'total': result[3], 'avatar': avatar(request)})

        except (IndexError, MultiValueDictKeyError) as e:
            if sort_flag == '1':
                products = Product.objects.all().order_by('-reviews')
            elif sort_flag == '2':
                products = Product.objects.all().order_by('price')
            elif sort_flag == '3':
                products = Product.objects.all().order_by('-feedback')
            elif sort_flag == '4':
                products = Product.objects.all().order_by('-date')
            else:
                products = Product.objects.select_related('category').select_related('shop').all()
            return render(request, 'catalog.html',
                          {'products': products, 'tags': tags_list(), 'categories': result[0],
                           'basket_product_count': result[2], 'total': result[3], 'avatar': avatar(request)})

    def post(self, request):
        """Принимает значение из строки поиска и формирует список
         подходящих товаров по частичному или полному совпадению"""

        result = base(request)
        search_products = Product.objects.select_related('category').select_related('shop').all()
        search_text = request.POST['query']
        products = []
        for search in search_products:
            if re.search(search_text.lower(), search.title.lower()) \
                    or re.search(search_text.lower(), search.description.lower()) \
                    or re.search(search_text.lower(), search.category.title.lower()):
                products.append(search)
        return render(request, 'catalog.html', {'products': products, 'tags': tags_list(), 'categories': result[0],
                                                'basket_product_count': result[2], 'total': result[3],
                                                'avatar': avatar(request)})
