from .base import *
from django.shortcuts import render, redirect
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
import re


class PaymentView(View):
    """Оплата картой"""

    def get(self, request):
        result = base(request)
        return render(request, 'payment.html', {'categories': result[0], 'basket_product_count': result[2],
                                                'total': result[3], 'id': request.GET['q'], 'avatar': avatar(request)})


class OnePaymentView(View):
    """Оплата случайной картой"""

    def get(self, request):
        result = base(request)
        return render(request, 'paymentsomeone.html', {'categories': result[0], 'basket_product_count': result[2],
                                                       'total': result[3], 'id': request.GET['q'],
                                                       'avatar': avatar(request)})


class ProgressPaymentView(View):
    """Валидация оплаты"""

    def post(self, request):
        result = base(request)
        history_id = int(request.build_absolute_uri().split('/')[-1:][0][3:])
        card_number = re.sub(r'(\d)\s+(\d)', r'\1\2', request.POST['numero1'])
        if int(request.POST['numero1'][-1]) != 0 and int(card_number) % 2 == 0:
            history_order = OrderHistory.objects.get(id=history_id)
            history_order.status = 'оплачен'
            history_order.save()
            payment_url = 'payment_yes'
        else:
            payment_url = 'payment_no'
        return render(request, 'progressPayment.html', {'categories': result[0], 'basket_product_count': result[2],
                                                        'total': result[3], 'payment_url': payment_url,
                                                        'avatar': avatar(request)})

    def get(self, request):
        return redirect('/')


class YesPaymentView(View):
    """Страница подтверждения успешной оплаты"""

    def get(self, request):
        result = base(request)
        return render(request, 'payment_yes.html', {'categories': result[0], 'basket_product_count': result[2],
                                                    'total': result[3], 'avatar': avatar(request)})


class NoPaymentView(View):
    """Страница отклонения оплаты"""

    def get(self, request):
        result = base(request)
        return render(request, 'payment_no.html', {'categories': result[0], 'basket_product_count': result[2],
                                                   'total': result[3], 'avatar': avatar(request)})
