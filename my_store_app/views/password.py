from django.shortcuts import render, redirect
from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import smtplib
import random


class MailView(View):
    """Страница ввода e-mail , для восстановления пароля"""

    def get(self, request):
        return render(request, 'e-mail.html')


class PasswordView(View):
    """Генерация нового пароля, перезапись парроля пользователя и отправка нового пароля ему на почту,
     для отправки необходимо войти в учетную запись https://myaccount.google.com/lesssecureapps"""

    def get(self, request):
        chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        password = ''
        for i in range(10):
            password += random.choice(chars)
        try:
            user_auth = User.objects.get(id=request.user.id)
            user_auth.set_password(password)
            user_auth.save()
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login('justkiddingboat@gmail.com', 'just123kidding')
            smtpObj.sendmail("justkiddingboat@gmail.com", request.GET['login'], str(password))
            smtpObj.quit()
        except ObjectDoesNotExist:
            print('пользователь не найден')
        return render(request, 'password.html')
