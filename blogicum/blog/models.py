from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreateAtMixin, IsPublishedMixin
from core.constants import (MAXLENGTH,
                            SHORT_TITLE_CATEGORY,
                            SHORT_TEXT_COMMENT,
                            SHORT_NAME_LOCATION,
                            SHORT_TITLE_POST
                            )


User = get_user_model()


class Location(CreateAtMixin, IsPublishedMixin):
    name = models.CharField(
        max_length=MAXLENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:SHORT_NAME_LOCATION]


class Category(CreateAtMixin, IsPublishedMixin):
    title = models.CharField(max_length=MAXLENGTH, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:SHORT_TITLE_CATEGORY]


class Post(CreateAtMixin, IsPublishedMixin):
    title = models.CharField(max_length=MAXLENGTH, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(
        'Изображение',
        upload_to='comments_images',
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — можно '
                   'делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:SHORT_TITLE_POST]


class Comment(CreateAtMixin):
    text = models.TextField('Текст коментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return (self.text[:SHORT_TEXT_COMMENT] + '...'
                if len(self.text) > SHORT_TEXT_COMMENT else self.text)
