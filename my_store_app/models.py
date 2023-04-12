from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from jsonfield import JSONField


class Delivery(models.Model):
    min_free_delivery = models.IntegerField(default=0, verbose_name='минимальня цена покупки')
    delivery_price = models.IntegerField(default=0, verbose_name='цена обычной доставки')
    express_delivery_price = models.IntegerField(default=0, verbose_name='цена экспресс доставки доставки')

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

    def __str__(self):
        return str(self.min_free_delivery)


class Profile(models.Model):
    """Модель пользователя и функция создания пользователя при создании суперюзера"""
    def validate_image(fieldfile_obj):
        """Валидация размера изображения при загрузке аватара пользователя"""
        file_size = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError("Максимальный размер файла {}MB".format(str(megabyte_limit)))

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(default='No name', max_length=50,
                                verbose_name='username', blank=True, null=True)
    full_name = models.CharField(default='не указано', max_length=50, verbose_name='ФИО пользователя', blank=True)
    phone = models.CharField(default='Не указано', max_length=30, verbose_name='номер телефона', blank=True, null=True,
                             unique=True)
    email = models.EmailField(verbose_name='email пользователя', blank=True, unique=True)
    avatar = models.ImageField(upload_to='static/', default='static/non.png', null=True,
                               validators=[validate_image])

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Profile.objects.create(user=instance)


class Sales(models.Model):
    """Товары по распродаже"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='магазин')
    count = models.IntegerField(default=0, verbose_name='количество товара по скидке')
    dateFrom = models.DateField(auto_now_add=True)
    dateTo = models.DateField(verbose_name='акция действует до')

    class Meta:
        verbose_name = 'Распродажа'
        verbose_name_plural = 'Распродажа'


class CategoryProduct(models.Model):
    """Категории товаров"""
    title = models.TextField(max_length=50, verbose_name='название категории')
    image = models.FileField(upload_to='static/', null=True,
                             default='static/4552614-design-illustration-image-picture_121395.svg')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    """Товар"""
    category = models.ForeignKey('CategoryProduct', on_delete=models.CASCADE, verbose_name='категория товара')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name='магазин товара')
    price = models.IntegerField(default=0, verbose_name='цена товара')
    discount = models.IntegerField(default=0, verbose_name='скидка % ')
    count = models.IntegerField(default=0, verbose_name='количество ')
    date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    title = models.TextField(max_length=50, verbose_name='название товара')
    description = models.TextField(max_length=1000, verbose_name='описание товара')
    limited_offer = models.BooleanField(default=False, verbose_name='ограниченное предложение')
    limited_offer_date = models.DateTimeField()
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченная серия')
    product_picture = models.ImageField(upload_to='static/', null=True, default='static/image_no_icon_216618.png')
    rating = models.IntegerField(default=0, verbose_name='счетчик покупок товара')
    reviews = models.IntegerField(default=0, verbose_name='счетчик просмотров  товара')
    tags = models.ManyToManyField('TagsFile', related_name='tags')
    feedback = models.IntegerField(default=0, verbose_name='счетчик комментариев')
    free_shipping = models.BooleanField(default=False)

    def plus_reviews(self):
        """Счетчик просмотра товара"""
        self.reviews += 1
        self.save()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Files(models.Model):
    """Изображения товара"""
    product = models.ForeignKey('Product', default=None, on_delete=models.CASCADE)
    file = models.FileField(upload_to='static/')


class TagsFile(models.Model):
    """Тэг"""
    tags_name = models.TextField(max_length=50, verbose_name='тэг товара')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.tags_name


class Feedback(models.Model):
    """Отзыв"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар',
                                related_name='product_title_product_set')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='пользователь')
    text = models.CharField(default='Не указано', max_length=100, verbose_name='текст отзыва', blank=True)
    create_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


@receiver(post_save, sender=Feedback)
def create_user_profile(sender, instance, created, **kwargs):
    """счетчик комментариев, при создании коментария в таблице товара увеличивается счетчик комментариев"""
    if created:
        product = Product.objects.get(id=instance.product_id)
        product.feedback += 1
        product.save()


class Shop(models.Model):
    """Магазин"""
    shop_name = models.TextField(max_length=50, verbose_name='название магазина')

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return self.shop_name


class Specifications(models.Model):
    """Спецификация товара (описание)"""
    specifications = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='товар')
    name = models.TextField(max_length=50, verbose_name='название')
    value = models.TextField(max_length=50, verbose_name='значение')

    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'

    def __str__(self):
        return self.name


class OrderHistory(models.Model):
    """История заказов пользователя"""
    user_order = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='пользователь', null=True)
    product = models.ManyToManyField('Product', related_name='order_product', through='OrderEnrollment')
    payment_date = models.DateField(auto_now_add=True)
    delivery_type = models.TextField(max_length=30, default='не указан', verbose_name='способ доставки')
    payment_type = models.TextField(max_length=30, default='не указан', verbose_name='способ оплаты')
    total_cost = models.IntegerField(default=0, verbose_name='общая стоимость заказа')
    status = models.TextField(max_length=30, default='не оплачен', verbose_name='статус оплаты')
    city = models.TextField(max_length=30, default='не указан', verbose_name='город доставки')
    address = models.TextField(max_length=30, default='не указан', verbose_name='адрес доставки')

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'Истории покупок'

    def __str__(self):
        return self.user_order.username


class OrderEnrollment(models.Model):
    """Промежуточная таблица связи истории пользователя с моделью товара"""
    order = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0, verbose_name='кол-во товаров')


class Basket(models.Model):
    """Корзина"""
    username = models.OneToOneField(Profile, unique=True, on_delete=models.CASCADE, related_name='profile')
    product = models.ManyToManyField('Product', related_name='product', through='Enrollment')
    create_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Enrollment(models.Model):
    """Промежуточная таблица связи корзины с моделью товара"""
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_count = models.IntegerField(default=0, verbose_name='кол-во товаров')


class Comparison(models.Model):
    """Сравнение товаров"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    username = models.TextField(max_length=100, default='не указан', verbose_name='токен пользователя ')


class AnonymousBasket(models.Model):
    """Корзина неавторизованного пользователя"""
    username_token = models.TextField(max_length=100, default='не указан', verbose_name='csrftoken  пользователя ')
    product = models.ManyToManyField('Product', related_name='anonumous_product', through='AnonymousEnrollment')
    create_at = models.DateField(auto_now_add=True)


class AnonymousEnrollment(models.Model):
    """Промежуточная таблица связи корзины неавторизованного пользователя с моделью товара"""
    basket = models.ForeignKey(AnonymousBasket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_count = models.IntegerField(default=0, verbose_name='кол-во товаров')


class UserCatalogFilter(models.Model):
    """Сохренение истории поиска пользователя"""
    user_filter = models.TextField(max_length=100, default='не указан', verbose_name='csrftoken  пользователя ')
    variable = JSONField()
