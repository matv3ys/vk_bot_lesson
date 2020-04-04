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
    response = vk.friends.get(fields='bdate')
    if response['items']:
        friends_list = []
        for i in response['items']:
            friend = [i['last_name'], i['first_name']]
            if 'bdate' in i:
                friend.append(i['bdate'])
            friends_list.append(friend)
        friends_list.sort(key=lambda x: x[0])
        for friend in friends_list:
            if len(friend) == 3:
                print(f'Фамилия: {friend[0]}, Имя: {friend[1]}, ДР: {friend[2]}')
            else:
                print(f'Фамилия: {friend[0]}, Имя: {friend[1]}, ДР: неизвестно')


if __name__ == '__main__':
    main()
