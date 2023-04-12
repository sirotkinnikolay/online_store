from django.views import View
from my_store_app.models import *
from my_store_app.forms import *
from django.http import HttpResponseRedirect


class CreateFeedbackView(View):
    """Создание отзыва о товаре, при отправке POST запроса со страницы товара"""

    def post(self, request):
        product_number = request.build_absolute_uri().split('/')[-1:][0][3:]
        feedback = request.POST['review']
        author_id = request.user.id
        if request.user.is_authenticated:
            Feedback.objects.create(product_id=product_number, author_id=author_id, text=feedback)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
