# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Product(models.Model):
    """Модель продукта"""

    name = models.TextField(
        blank=True,
        null=True,
        verbose_name='Название',
    )
    price = models.TextField(
        blank=True,
        null=True,
        verbose_name='Цена',
    )
    image = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    class Meta:
        managed = False
        db_table = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class User(models.Model):
    """Модель пользователя"""

    first_name = models.TextField(
        blank=True,
        null=True,
        verbose_name='Имя',
    )
    last_name = models.TextField(
        blank=True,
        null=True,
        verbose_name='Фамилия',
    )
    email = models.TextField(
        blank=True,
        null=True,
        verbose_name='Почта',
    )

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
