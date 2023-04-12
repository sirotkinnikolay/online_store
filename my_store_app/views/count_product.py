from .base import *
from django.shortcuts import redirect
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *


class CountProductPlus(View):
    """Изменение количества товара в корзине,
     если пользователь изменил кнопками на странице cart.html"""

    def post(self, request):
        result = base(request)
        count_object = zip(result[1], request.POST.getlist('amount'))
        for old, new in count_object:
            old.product_count = new
            old.save()
        return redirect('/order/')
