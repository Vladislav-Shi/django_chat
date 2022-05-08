'''
Это синхронный потребитель WebSocket, который принимает все соединения, 
получает сообщения от своего клиента и отправляет эти сообщения обратно 
тому же клиенту. На данный момент он не передает сообщения другим 
клиентам в той же комнате.
'''
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatModel, ChatUser, MessageModel


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.chat = await self.get_chat()
        self.messages_story = await self.get_message_story()
        print('self.messages_story', self.messages_story)

        # Пользователь подключился
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        # Отправляет сообщение тольок для одного пользователя
        await self.send(text_data=json.dumps({
            'message': 'hello here!'
        }))

    async def disconnect(self, close_code):
        # Пользователь покинул комнату
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получает сообщение от web-socket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Сообщение каждому в чате
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.add_message_to_db(message, username)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    '''
    ###########################################################################
    методы рабоыт с бд
    '''
    @database_sync_to_async
    def get_chat(self):
        '''
        Возвращает чат
        Отдельно потому что может просилдать нагрузка если каждый раз просить
        '''
        return ChatModel.objects.get(slug=self.room_name)

    @database_sync_to_async
    def get_message_story(self):
        '''
        Получает историю сообщений текущего чата
        '''
        return list(self.chat.message.all())

    @database_sync_to_async
    def add_message_to_db(self, message, username):
        '''
        метод записывает сообщение в базу данных
        '''
        user = ChatUser.objects.get(username = username)
        message =  MessageModel(message = message, publisher= user, chat = self.chat)
        message.save()

