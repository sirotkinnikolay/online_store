from .base import *
from django.shortcuts import render, redirect
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


class CartView(View):
    """Корзина пользователя, удаление количества товара, подсчет общей стоимости корзины"""

    def get(self, request):
        result = base(request)
        total_price_cart = 0
        if request.user.is_authenticated:
            user_pr = Profile.objects.get(id=request.user.id)
            bask = Basket.objects.get(username=user_pr)
            cart_user = bask.product.all()
            for prod_price in cart_user:
                prod_enroll_count = Enrollment.objects.get(basket_id=bask, product_id=prod_price.id).product_count
                if prod_enroll_count != 0:
                    total_price_cart += int(prod_price.price) * prod_enroll_count
            enroll = Enrollment.objects.filter(basket_id=bask.id)
            cart = zip(cart_user, enroll)
        else:
            bask = AnonymousBasket.objects.get(username_token=request.COOKIES.get('csrftoken'))
            cart_user = bask.product.all()
            for prod_price in cart_user:
                prod_enroll_count = AnonymousEnrollment.objects.get(basket_id=bask,
                                                                    product_id=prod_price.id).product_count
                if prod_enroll_count != 0:
                    total_price_cart += int(prod_price.price) * prod_enroll_count
            enroll = AnonymousEnrollment.objects.filter(basket_id=bask.id)
            cart = zip(cart_user, enroll)

        return render(request, 'cart.html', {'cart': cart, 'total_price_cart': total_price_cart,
                                             'categories': result[0], 'basket_product_count': result[2],
                                             'total': result[3], 'avatar': avatar(request)})


class CartDeleteProductView(View):
    """Удаление категории товаров из корзины пользователя"""

    def get(self, request):
        sort_flag = request.GET['q']
        answer = sort_flag.split('-')
        if answer[0] == "del":
            if request.user.is_authenticated:
                user_pr = Profile.objects.get(id=request.user.id)
                bask = Basket.objects.get(username=user_pr)
                Enrollment.objects.get(basket_id=bask.id,
                                       product_id=answer[1]).delete()
            else:
                bask = AnonymousBasket.objects.get(username_token=request.COOKIES.get('csrftoken'))
                AnonymousEnrollment.objects.get(basket_id=bask.id,
                                                product_id=answer[1]).delete()
        return redirect('/cart/')


class AddProductCart(View):
    """Добавление товара в корзину зарегистрированного и анонимного пользователя,
     редирект на страницу с которой добавляется товар"""

    def get(self, request):
        product_add_id = int(request.GET['q'])
        if request.user.is_authenticated:
            user_pr = Profile.objects.get(id=request.user.id)
            bask = Basket.objects.get(username=user_pr)
            try:
                plus_count = Enrollment.objects.get(product_id=product_add_id, basket_id=bask.id)
                if plus_count:
                    plus_count.product_count = plus_count.product_count + 1
                    plus_count.save()
            except ObjectDoesNotExist:
                Enrollment.objects.create(basket_id=bask.id,
                                          product_id=product_add_id, product_count=1)
        else:
            bask = AnonymousBasket.objects.get(username_token=request.COOKIES.get('csrftoken'))
            try:
                plus_count = AnonymousEnrollment.objects.get(product_id=product_add_id, basket_id=bask.id)
                if plus_count:
                    plus_count.product_count = plus_count.product_count + 1
                    plus_count.save()
            except ObjectDoesNotExist:
                AnonymousEnrollment.objects.create(basket_id=bask.id,
                                                   product_id=product_add_id, product_count=1)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
