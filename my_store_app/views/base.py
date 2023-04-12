from my_store_app.models import *
from my_store_app.forms import *
import re
from django.core.exceptions import ObjectDoesNotExist


def base(request):
    """Функция для вывода информации в header"""
    base_item = []
    categories = CategoryProduct.objects.all()
    if request.user.is_anonymous:
        if len(AnonymousBasket.objects.filter(username_token=request.COOKIES.get('csrftoken'))) == 0:
            AnonymousBasket.objects.create(username_token=request.COOKIES.get('csrftoken'))
        enroll = AnonymousEnrollment.objects.filter(basket_id=AnonymousBasket.objects.
                                                    get(username_token=request.COOKIES.get('csrftoken')).id)
    else:
        enroll = Enrollment.objects.filter(basket_id=Basket.objects.get(username_id=request.user.id).id)

    basket_product_count = len(enroll)
    total = 0
    for price in enroll:
        total += (price.product.price * price.product_count)
    base_item.extend((categories, enroll, basket_product_count, total))
    return base_item


def avatar(request):
    try:
        profile_image = Profile.objects.get(id=request.user.id).avatar
    except ObjectDoesNotExist:
        profile_image = None
    return profile_image


def tags_list():
    """Функция вывода всех тэгов"""
    tags_ls = []
    for i in Product.objects.all():
        for n in i.tags.all():
            if n.tags_name not in tags_ls:
                tags_ls.append(n.tags_name)
    return tags_ls


def filter_result_objects(request_filter):
    """Функция фильтрации товаров для get и post запроса"""
    search_products = Product.objects.select_related('category').select_related('shop').all()
    first_filter = []
    for search in search_products:
        if re.search(request_filter['title'].lower(), search.title.lower()) \
                and int(request_filter['price'].split(';')[0]) <= search.price \
                <= int(request_filter['price'].split(';')[1]):
            first_filter.append(search)
    second_filter = []
    if 'chb2' in request_filter.keys():
        for element in first_filter:
            if element.free_shipping:
                second_filter.append(element)
    else:
        second_filter.extend(first_filter)
    third_filter = []
    if 'chb1' in request_filter.keys():
        for element in second_filter:
            if element.count >= 1:
                third_filter.append(element)
    else:
        third_filter.extend(second_filter)
    return third_filter
