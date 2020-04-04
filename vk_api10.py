import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime

TOKEN = ''
GROUP_ID = ''


def main(token, group_id):
    def greet(vk):
        text = '''Здравствуйте, я умею определять день недели по дате!
        Отправьте дату в формате YYYY-MM-DD'''
        vk.messages.send(user_id=event.obj.message['from_id'],
                         message=text,
                         random_id=random.randint(0, 2 ** 64))

    weekdays = {0: 'Понедельник',
                1: 'Вторник',
                2: 'Среда',
                3: 'Четверг',
                4: 'Пятница',
                5: 'Суббота',
                6: 'Воскресенье'
                }

    vk_session = vk_api.VkApi(
        token=token)

    longpoll = VkBotLongPoll(vk_session, group_id=group_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            message = event.obj.message['text']
            if len(message) == 10:
                if message[4] == '-' and message[7] == '-':
                    try:
                        ymd = [int(i) for i in message.split('-')]
                        day = weekdays[datetime.date(ymd[0], ymd[1], ymd[2]).weekday()]
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=day,
                                         random_id=random.randint(0, 2 ** 64))
                    except ValueError:
                        greet(vk)
                else:
                    greet(vk)
            else:
                greet(vk)


if __name__ == '__main__':
    main(TOKEN, GROUP_ID)
