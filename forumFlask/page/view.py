from flask import Blueprint, render_template, request
from forumFlask.models import Post
from flask_login import login_required


pageBp = Blueprint('pageBp', __name__)


# 2 routes handled by same function
@pageBp.route('/')
@pageBp.route('/home')
@login_required
def home():
    # get the page number in url to get the specific page (default 1)
    #pageN = request.args.get('page', 1, type=int)
    # use sqlAlchemy to paginate posts   order the post to latest at top   set page size to 6     
    posts = Post.query.order_by(Post.date.desc()).paginate(per_page=6)
    
    return render_template('home.html', post=posts)

@pageBp.route('/about')
def about():
   return render_template('about.html', title='About')
