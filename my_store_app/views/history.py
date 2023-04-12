from .base import *
from django.shortcuts import render
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *


class HistoryView(View):
    """Страница просмотра истории заказов пользователя"""

    def get(self, request):
        result = base(request)
        history_order = OrderHistory.objects.filter(user_order_id=request.user.id)
        return render(request, 'historyorder.html', {'categories': result[0], 'basket_product_count': result[2],
                                                     'total': result[3], 'history_order': history_order,
                                                     'avatar': avatar(request)})
