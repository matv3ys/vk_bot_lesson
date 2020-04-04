import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

TOKEN = ''
GROUP_ID = ''


def main(token, group_id):
    vk_session = vk_api.VkApi(
        token=token)

    longpoll = VkBotLongPoll(vk_session, group_id=group_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user_id = event.obj.message['from_id']
            info = vk.users.get(user_ids=user_id, fields='bdate, city')[0]
            text = f'Привет, {info["first_name"]}!'
            if 'city' in info:
                text += f' Как поживает {info["city"]["title"]}?'
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=text,
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main(TOKEN, GROUP_ID)