import json
from pathlib import Path

home = Path.home()
path = Path(home, 'PycharmProjects', 'Ipatov_hw12', 'posts.json')


def load_from_json(path):
    """Возвращает список постов"""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def search_posts(search_query):
    """Находит посты и добавляет в список search_list"""
    search_list = []
    for post_list in load_from_json(path):
        if search_query.lower() in post_list['content'].lower():
            search_list.append(post_list)
    return search_list


def save_picture(picture):
    """Загружает картинку по адресу ./uploads/images/{filename}"""
    filename = picture.filename
    path = f"./uploads/images/{filename}"
    picture.save(path)
    return path


def add_post(post):
    """Добавляет пост в posts.json"""
    posts = load_from_json(path)
    posts.append(post)
    with open("posts.json", "w", encoding="utf-8") as file:
        json.dump(posts, file)
    return posts
