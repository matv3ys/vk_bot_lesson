import vk_api
import os

LOGIN = ''
PASSWORD = ''
ALBUM_ID = ''
GROUP_ID = ''


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    upload = vk_api.VkUpload(vk_session)

    for photo in os.listdir(path='static\\img'):
        photo_path = os.path.join('static\\img', photo)
        upload.photo(photo_path, album_id=ALBUM_ID, group_id=GROUP_ID)


if __name__ == '__main__':
    main()
