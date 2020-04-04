import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from datetime import datetime
import pytz

TOKEN = ''
GROUP_ID = ''


def main(token, group_id):
    def greet(vk, id):
        text = '''Здравствуйте, я могу подсказать время'''
        vk.messages.send(user_id=id,
                         message=text,
                         random_id=random.randint(0, 2 ** 64))

    keys = {'время', 'число', 'дата', 'день'}

    vk_session = vk_api.VkApi(
        token=token)

    longpoll = VkBotLongPoll(vk_session, group_id=group_id)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            message = event.obj.message['text'].lower()
            id = event.obj.message['from_id']
            if keys.intersection(set(message.split())):
                tzmoscow = pytz.timezone('Europe/Moscow')
                now = str(datetime.now(tzmoscow))[0:19]
                vk.messages.send(user_id=id,
                                 message=now,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                greet(vk, id)


if __name__ == '__main__':
    main(TOKEN, GROUP_ID)
