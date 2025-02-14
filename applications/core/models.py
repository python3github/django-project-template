import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible
from model_utils import Choices


class Common(models.Model):
    """
    Абстрактный класс. Содержит `статус` и `время создания / модификации` объекта.
    """

    STATUS = Choices(
        (0, 'draft', 'Черновик'),
        (1, 'published', 'Опубликовано'),
    ) # yapf: disable

    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=STATUS,
        default=STATUS.published,
        max_length=50,
    )

    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    modified = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created']


class MetaFields(models.Model):
    """
    Абстрактный класс. Содержит мета описание и ключевые слова.
    """

    meta_description = models.CharField(
        verbose_name='META описание',
        max_length=200,
        help_text='Рекомендуемая длина мета описания = 160 символов.',
        blank=True,
        null=True,
    )

    meta_keywords = models.CharField(
        verbose_name='META ключевые слова',
        max_length=2500,
        help_text='Укажите ключевые слова через запятую.',
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        _, extension = os.path.splitext(filename)
        filename = '{}{}'.format(uuid.uuid4().hex, extension)
        return os.path.join(self.path, filename)
