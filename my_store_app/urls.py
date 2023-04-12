from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', CategoryView.as_view(), name='index'),
    path('register/', register_view, name='register'),
    path('logout/', AuthorLogoutView.as_view(), name='logout'),
    path('login/', Login.as_view(template_name='login.html'), name='login'),
    path('product/<int:pk>/', ProductdView.as_view(), name='one_product'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    path('edit_profile/', AccountUpdateView.as_view(), name='edit_profile'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('about/', AboutView.as_view(), name='about'),
    path('sale/', SaleView.as_view(), name='sale'),
    path('user_office/<int:pk>/', UserOfficeView.as_view(), name='user_office'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete/', CartDeleteProductView.as_view(), name='cart_delete'),
    path('cart/add/', AddProductCart.as_view(), name='cart_add'),
    path('mail/', MailView.as_view(), name='mail'),
    path('password/', PasswordView.as_view(), name='password'),
    path('create/feedback/', CreateFeedbackView.as_view(), name='feedback'),
    path('order/', OrderView.as_view(), name='order'),
    path('oneorder/<int:pk>/', OneOrderView.as_view(), name='one_order'),
    path('history/', HistoryView.as_view(), name='history'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('paymentsomeone/', OnePaymentView.as_view(), name='paymentsomeone'),
    path('progresspayment/', ProgressPaymentView.as_view(), name='progresspayment'),
    path('payment_yes/', YesPaymentView.as_view(), name='payment_yes'),
    path('payment_no/', NoPaymentView.as_view(), name='payment_no'),
    path('comparison/', ComparisonView.as_view(), name='comparison'),
    path('add_comparison/', AddComparisonView.as_view(), name='add_comparison'),
    path('filter_catalog/', FilterCatalogView.as_view(), name='filter_catalog'),
    path('count_plus/', CountProductPlus.as_view(), name='count_plus'),
    path('registr_login_default/', LoginDefault.as_view(), name='registr_login_default'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
