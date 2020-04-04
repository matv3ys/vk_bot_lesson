import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import wikipedia

TOKEN = ''
GROUP_ID = ''


def main(token, group_id):
    greet = False

    vk_session = vk_api.VkApi(
        token=token)

    longpoll = VkBotLongPoll(vk_session, group_id=group_id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            id = event.obj.message['from_id']
            message = event.obj.message['text']
            try:
                wikipedia.set_lang('ru')
                search = wikipedia.WikipediaPage(message)
                url = search.url
                content = search.content[0:500] + '...'
                text = '\n'.join([url, content])
            except wikipedia.exceptions.PageError:
                text = 'Ничего не найдено'
            except wikipedia.exceptions.DisambiguationError as e:
                text = 'Попробуйте уточнить запрос'
            vk.messages.send(user_id=id,
                             message=text,
                             random_id=random.randint(0, 2 ** 64))

        if event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            if not greet:
                greet = True
                vk = vk_session.get_api()
                id = event.obj['from_id']
                text = '''Здравствуйте, чем вы интересуетесь?'''
                vk.messages.send(user_id=id,
                                 message=text,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main(TOKEN, GROUP_ID)
