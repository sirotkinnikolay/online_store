from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.models import User
from django.db import IntegrityError


def register_view(request):
    """Функция регистрации нового пользователя"""

    if request.method == 'POST':
        form = AuthorRegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('login')
            try:
                user = User.objects.create_user(username=username, first_name=full_name, email=email)
            except IntegrityError:
                return redirect('/registr_login_default/')
            user.set_password(raw_password)
            user.save()
            login(request, user)
            user_profile = Profile.objects.create(user=user, username=username, full_name=full_name, phone=phone,
                                                  email=email)
            Basket.objects.create(username=user_profile)
        return redirect('/')
    return render(request, 'registr.html')


class AuthorLogoutView(LogoutView):
    """Выход из учетной записи"""

    next_page = '/'


class Login(LoginView):
    """Вход в учетную запись"""

    def form_valid(self, form):
        """Если пользователь заходит с неаутефицированного пользователя, у которого в корзине были товары,
         то его корзина заполняется товарами которые он добавил до входа, корзина
          анонимного пользователя опустошается"""

        if len(AnonymousEnrollment.objects.filter(
                basket=AnonymousBasket.objects.get(username_token=self.request.COOKIES.get('csrftoken')))) != 0:
            get_user = Profile.objects.get(username=form.cleaned_data['username'])
            get_basket = Basket.objects.get(username=get_user)
            get_enroll = Enrollment.objects.filter(basket_id=get_basket.id)
            get_enroll.delete()
            for enroll_new in AnonymousEnrollment.objects.filter(basket_id=AnonymousBasket.objects.get(
                    username_token=self.request.COOKIES.get('csrftoken')).id):
                Enrollment.objects.create(basket=get_basket, product=enroll_new.product,
                                          product_count=enroll_new.product_count)
                enroll_new.delete()

        return super().form_valid(form)


class LoginDefault(View):
    """Страница регистрации , если логин или email занят"""

    def get(self, request):
        return render(request, 'registr_login_default.html')
