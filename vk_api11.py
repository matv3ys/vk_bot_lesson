import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import json
from get_map import get_coords, get_map
from requests import post

TOKEN = ''
GROUP_ID = '193246121'

first = []
correct = []
map_params = {}


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


keyboard = {
    "one_time": True,
    "buttons": [
        [
            get_button(label="схема", color="positive"),
            get_button(label="спутник", color="primary"),
            get_button(label="гибрид", color="negative"),
        ]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def main(token, group_id):
    global first, correct, map_params
    vk_session = vk_api.VkApi(
        token=token)

    longpoll = VkBotLongPoll(vk_session, group_id=group_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            message = event.obj.message['text']
            if event.obj.message['from_id'] not in first:
                text = f'Привет, введи название местности которую ты хочешь увидеть!'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=text,
                                 random_id=random.randint(0, 2 ** 64))
                first.append(event.obj.message['from_id'])
                continue

            if event.obj.message['from_id'] not in correct:
                cur_map_params = get_coords(message)
                if cur_map_params:
                    map_params[event.obj.message['from_id']] = cur_map_params
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Отлично, выберите тип карты",
                                     keyboard=keyboard,
                                     random_id=random.randint(0, 2 ** 64))
                    correct.append(event.obj.message['from_id'])
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Ничего не найдено, попробуйте ещё",
                                     random_id=random.randint(0, 2 ** 64))
                continue

            if 'схема' in message or 'спутник' in message or 'гибрид' in message:
                cur_map_params = map_params[event.obj.message['from_id']]
                if 'схема' in message:
                    cur_map_params["l"] = 'map'
                    type = 'map'
                elif 'спутник' in message:
                    cur_map_params["l"] = 'sat'
                    type = 'sat'
                elif 'гибрид' in message:
                    cur_map_params["l"] = 'skl'
                    type = 'skl'

                user_id = event.obj.message['from_id']
                fname = get_map(cur_map_params, type, user_id)

                serv = vk.photos.getMessagesUploadServer(peer_id=event.obj.message['from_id'])
                post_1 = post(serv['upload_url'], files={'photo': open(fname, 'rb')}).json()

                save = vk.photos.saveMessagesPhoto(server=post_1['server'], photo=post_1['photo'], hash=post_1['hash'])[
                    0]

                photo_name = f'photo{save["owner_id"]}_{save["id"]}'

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Найдено, хотите поискать ещё что-нибудь?',
                                 attachment=photo_name,
                                 random_id=random.randint(0, 2 ** 64))

                del map_params[event.obj.message['from_id']]
                correct.remove(event.obj.message['from_id'])


            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Неверно выбран тип карты",
                                 keyboard=keyboard,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main(TOKEN, GROUP_ID)
