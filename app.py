import logging
from json import JSONDecodeError
from flask import Flask, request, render_template
from functions import search_posts, save_picture, add_post, Path
from main.utils import main_blueprint
from loader.utils import loader_blueprint


app = Flask(__name__)


app.register_blueprint(main_blueprint) #Подтягивание блупринта main_blueprint
app.register_blueprint(loader_blueprint) #Подтягивание блупринта loader_blueprint

logging.basicConfig(filename='log.log', level=logging.INFO) #Добавление логгирования


@app.route("/search/")
def search_page():
    """Вьюшка для поиска"""
    search_query = request.args.get('s', '')
    logging.info('Searching...')
    try:
        posts = search_posts(search_query)
        return render_template('post_list.html', search_query=search_query, posts=posts)
    except FileNotFoundError:
        logging.error('File not found')
        return "File not found"
    except JSONDecodeError:
        logging.error('Invalid file')
        return "Invalid file"


@app.route("/post/", methods=["POST"])
def page_post_upload():
    """Вьюшка для добавления поста"""
    picture = request.files.get("picture")
    content = request.form.get("content")
    logging.info('Downloading...')
    if not picture:
        return 'Upload a picture!'
    elif Path(picture.filename).suffix != '.jpeg' or '.png' or '.jpg':
        logging.info('Download file is not an image!')
        return 'Download file is not an image!'
    elif not content:
        return 'No content'
    else:

        try:
            picture_path = "/" + save_picture(picture)
        except FileNotFoundError:
            logging.error('File not found')
            return "File not found"
        except JSONDecodeError:
            logging.error('Invalid file')
            return "Invalid file"

        post = add_post({"pic": picture_path, "content": content})
        return render_template('post_uploaded.html', post=post)


app.run()
