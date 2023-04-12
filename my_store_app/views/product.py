from .base import *
from django.views.generic import DetailView
from my_store_app.models import *
from my_store_app.forms import *


class ProductdView(DetailView):
    """Страница информации об одном товаре product.html"""

    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductdView, self).get_context_data(**kwargs)
        result = base(self.request)
        tags_ls = []
        picture_list = Files.objects.filter(product_id=self.kwargs['pk'])[:3]
        specification_list = Specifications.objects.filter(specifications_id=self.kwargs['pk'])
        feedbacks = Feedback.objects.filter(product_id=self.kwargs['pk'])

        for i in Product.objects.filter(id=self.kwargs['pk']):
            for n in i.tags.all():
                tags_ls.append(n.tags_name)
        context['tags'] = tags_ls
        context['files'] = picture_list
        context['specif'] = specification_list
        context['categories'] = result[0]
        context['feedbacks'] = feedbacks
        context['product_id'] = self.kwargs['pk']
        context['len_feedbacks'] = feedbacks.count()
        context['basket_product_count'] = result[2]
        context['total'] = result[3]
        context['avatar'] = avatar(self.request)
        return context

    def get_object(self, queryset=None):
        """Счетчик просмотров товара (reviews)"""
        item = super().get_object(queryset)
        item.plus_reviews()
        return item
