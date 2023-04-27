from flask import Flask
from flask_flatpages import FlatPages
from flask import render_template , send_from_directory
import os

FLATPAGES_EXTENSION = '.md'
#FLATPAGES_MARKDOWN_EXTENSIONS = ['extra']
FLATPAGES_AUTO_RELOAD = True

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/wwfs'
app.config.from_object(__name__)
pages = FlatPages(app)

pages.get('foo')
application = app

def Liste_cat():
    articles = (p for p in pages if 'published' in p.meta)
    catList = []
    for a in articles:
        catList.append(a.meta['cat'])
    catList = list(dict.fromkeys(catList))
    return catList

def imagelist(articlename):
    dir_path = os.path.dirname(os.path.realpath(articlename))+'/pages/'
    gallery_path = os.path.join(dir_path, articlename)
    if os.path.exists(gallery_path):
        images = [f for f in os.listdir(gallery_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif')]
        print(images)
        return gallery_path ,images
    else:
        return None, None

@app.route('/pages/<path:path>')
def serve_pages(path):
    return send_from_directory('pages', path)

@app.route('/')
def index():
    # Articles are pages with a publication date
    articles = (p for p in pages if 'published' in p.meta)
    # Show the 10 most recent articles, most recent first.
    catList = Liste_cat()
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('base.html', articles=latest , catList=catList)

@app.route('/<path:path>')
def page(path):
    g_path , imgs = imagelist(path)
    print(imgs)
    page = pages.get_or_404(path)
    if imgs:
        return render_template('single.html', page=page  , g_path=g_path, imgs = imgs)
    else :
        return render_template('single.html', page=page )

@app.route('/cat/<cate>')
def catPage(cate):
    articles = (p for p in pages if 'published' in p.meta and p.meta['cat']==cate )
    catList = Liste_cat()
    latest = sorted(articles , reverse=True , key=lambda p: p.meta['published'])
    return render_template('base.html', latest=latest , catList=catList)

@app.route('/s/<path:patht>')
def statPage(path):
    articles = (p for p in pages if 'published' in p.meta)
    page = pages.get_or_404(path)
    return render_template('statpage.html' , page=page)
