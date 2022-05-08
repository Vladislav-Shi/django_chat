from django.db import models
from django.contrib.auth.models import AbstractUser


class ChatModel(models.Model):
    '''
    Класс который хранит чат
    '''
    chat_name = models.CharField(verbose_name='Название чата', max_length=40)
    slug = models.SlugField(verbose_name='slug чата', max_length=40, unique=True)

    def __str__(self) -> str:
        return str(self.pk) + ': ' + self.slug


class MessageModel(models.Model):
    '''
    Таблица котораяч хранит сообщения от пользователей
    '''
    message = models.TextField(verbose_name='текст сообщения')
    # для вложений наверное можно использвоаеть JSON (так как вложений может быть много)
    attacment = models.JSONField(verbose_name='Обьект со вложениями', blank=True, null=True)
    time = models.DateTimeField(
        verbose_name='Время отправки', db_index=True, auto_now=True)
    publisher = models.ForeignKey(
        verbose_name='Автор сообщения', to='ChatUser', on_delete=models.CASCADE)
    chat = models.ForeignKey(
        verbose_name='Чат в котором сообщение', to='ChatModel', on_delete=models.CASCADE,
        related_name='message')


class UploadFIleModel(models.Model):
    '''
    Таблица которая хранит вложение принадлежащее сообщениям
    '''
    pass


class ChatUser(AbstractUser):
    '''
    Переопределяем класс юзера
    '''
    photo = models.ImageField(
        verbose_name='Фото пользователя',
        blank=True, null=True,
        upload_to='user/')
    chat = models.ManyToManyField(
        to='ChatModel', verbose_name='Чаты ползователя')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
