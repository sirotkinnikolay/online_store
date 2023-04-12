from .base import *
from django.views import View
from django.views.generic import DetailView
from my_store_app.models import *
from my_store_app.forms import *
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class AccountView(DetailView):
    """Страница информации о пользователе"""

    model = Profile
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        result = base(self.request)
        context['categories'] = result[0]
        context['basket_product_count'] = result[2]
        context['total'] = result[3]
        context['avatar'] = avatar(self.request)
        return context


class AccountUpdateView(View):
    """Изменение данных пользователя через форму на странице profile.html"""

    def post(self, request):
        user = Profile.objects.get(id=request.user.id)

        if 'avatar' in request.FILES.keys():
            avatar_image = request.FILES['avatar']
            user.avatar.save(avatar_image.name, avatar_image)

        user_auth = User.objects.get(id=request.user.id)
        user_auth.first_name = request.POST['name']
        user_auth.email = request.POST['mail']
        user.phone = request.POST['phone']
        user.full_name = request.POST['name']
        user.email = request.POST['mail']

        if request.POST['password'] == '' or request.POST['passwordReply'] == '':
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if request.POST['password'] == request.POST['passwordReply']:
            user_auth.set_password(str(request.POST['password']))

        user.save()
        user_auth.save()
        login(request, user_auth)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
