# Generated by Django 4.1.7 on 2023-03-16 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store_app', '0003_alter_product_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='limited_edition',
            field=models.BooleanField(default=False, verbose_name='ограниченная серия'),
        ),
        migrations.AlterField(
            model_name='product',
            name='limited_offer',
            field=models.BooleanField(default=False, verbose_name='ограниченное предложение'),
        ),
    ]