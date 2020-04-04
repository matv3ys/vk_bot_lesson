import vk_api
import datetime


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    # Используем метод wall.get
    response = vk.wall.get(count=5, offset=1)
    if response['items']:
        for i, j in enumerate(response['items']):
            print(f'{i + 1}:\t{j["text"]}')
            unix_time = j['date']
            date_time = datetime.datetime.fromtimestamp(unix_time)
            print(f'  \tdate: {date_time.date()}, time: {date_time.time()}')


if __name__ == '__main__':
    main()
