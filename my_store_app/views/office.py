from .base import *
from django.views.generic import DetailView
from my_store_app.models import *
from my_store_app.forms import *


class UserOfficeView(DetailView):
    """Личный кабинет пользователя с заказами"""

    model = Profile
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super(UserOfficeView, self).get_context_data(**kwargs)
        result = base(self.request)
        history_order = OrderHistory.objects.filter(user_order_id=self.request.user.id)
        context['categories'] = result[0]
        context['basket_product_count'] = result[2]
        context['total'] = result[3]
        context['history_order'] = history_order
        context['avatar'] = avatar(self.request)
        return context
