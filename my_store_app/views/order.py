from .base import *
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class OrderView(View):
    """Оформление заказа, ввод данных о доставке, оплате"""

    def get(self, request):
        result = base(request)
        if request.user.is_authenticated:
            profile_info = Profile.objects.get(user_id=request.user.id)
        else:
            profile_info = []
        return render(request, 'order.html', {'categories': result[0], 'basket_product_count': result[2],
                                              'total': result[3], 'profile_info': profile_info,
                                              'enroll_order': result[1], 'avatar': avatar(request)})

    def post(self, request):
        """Сохранение истории покупки , данные с оформления корзины пользователя, после корзина опустошается,
        редирект на страницу данного заказа)"""

        if request.user.is_anonymous:
            full_name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['mail']
            raw_password = request.POST['password']
            username = request.POST['login']
            user = User.objects.create_user(username=username, first_name=full_name, email=email)
            user.set_password(raw_password)
            user.save()
            login(request, user)
            anon_user = Profile.objects.create(user=user, username=username, full_name=full_name, phone=phone,
                                               email=email)
            anon_basket = Basket.objects.create(username=anon_user)
            for enroll_new in AnonymousEnrollment.objects.filter(basket_id=AnonymousBasket.objects.get(
                    username_token=request.COOKIES.get('csrftoken')).id):
                Enrollment.objects.create(basket=anon_basket, product=enroll_new.product,
                                          product_count=enroll_new.product_count)

        delivery = request.POST['delivery']
        payment_type = request.POST['pay']
        city = request.POST['city']
        address = request.POST['address']

        basket_new = Basket.objects.get(username_id=request.user.id)
        enroll = Enrollment.objects.filter(basket_id=basket_new.id)
        delivery_parameter = Delivery.objects.first()
        total = 0
        for price in enroll:
            total += (price.product.price * price.product_count)
        if total < delivery_parameter.min_free_delivery and delivery == 'ordinary':
            total += delivery_parameter.delivery_price
        elif total < delivery_parameter.min_free_delivery and delivery == 'express':
            total += delivery_parameter.express_delivery_price
        order = OrderHistory.objects.create(user_order_id=request.user.id, delivery_type=delivery,
                                            payment_type=payment_type, city=city, address=address, total_cost=total)
        for order_enroll in enroll:
            OrderEnrollment.objects.create(order_id=order.id, product_id=order_enroll.product_id,
                                           count=order_enroll.product_count)
        enroll.delete()
        return redirect(f'/oneorder/{order.id}/')


class OneOrderView(DetailView):
    """Страница одного заказа"""

    model = OrderHistory
    template_name = 'oneorder.html'

    def get_context_data(self, **kwargs):
        context = super(OneOrderView, self).get_context_data(**kwargs)
        categories = CategoryProduct.objects.all()
        basket_product_count = 0
        total = 0
        history_order = OrderHistory.objects.get(id=self.kwargs['pk'])
        delivery_parameter = Delivery.objects.first()
        if history_order.payment_type == 'online':
            href = 'payment'
        else:
            href = 'paymentsomeone'
        if history_order.total_cost >= delivery_parameter.min_free_delivery:
            context['delivery'] = 0
        elif history_order.delivery_type == 'ordinary' and history_order.total_cost <\
                delivery_parameter.min_free_delivery:
            context['delivery'] = delivery_parameter.delivery_price
        elif history_order.delivery_type == 'express' and history_order.total_cost <\
                delivery_parameter.min_free_delivery:
            context['delivery'] = delivery_parameter.express_delivery_price
        products = OrderEnrollment.objects.filter(order_id=history_order.id)
        context['categories'] = categories
        context['basket_product_count'] = basket_product_count
        context['total'] = total
        context['order'] = history_order
        context['products'] = products
        context['total_order'] = history_order.total_cost
        context['href'] = href
        context['his_id'] = history_order.id
        return context
