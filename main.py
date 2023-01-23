import json
import sys

from flask import Flask, render_template, request
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PORT_DIR = 'portfolio'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route("/", methods=['post', 'get'])
def index():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)

    cards = [p for p in flatpages if p.path.startswith(PORT_DIR)]
    cards.sort(key=lambda item: item['title'])

    with open('settings.json', encoding='utf-8') as config:
        data = config.read()
        settings = json.loads(data)

    with open("about_text.txt", encoding='utf-8') as txt:
        readed_text = txt.readlines()
        about = []

        for line in readed_text:
            about.append(line)


    tags = set()

    for p in flatpages:
        t = p.meta.get('tag')

        if t:
            tags.add(t.lower())

    return render_template('index.html', posts=posts, cards=cards, bigheader=True, **settings, tags=tags, about=about)


@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)

    return render_template('post.html', post=post)


@app.route('/portfolio/<name>/')
def card(name):
    path = '{}/{}'.format(PORT_DIR, name)
    card = flatpages.get_or_404(path)

    return render_template('card.html', card=card)


@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=7777, debug=DEBUG)

