from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from forumFlask.post.form import PostForm
from forumFlask import db
from forumFlask.models import Post
from flask_login import current_user, login_required



postBp = Blueprint('postBp', __name__)


@postBp.route('/post/new', methods = ['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #save posts
        newPost = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(newPost)
        db.session.commit()
        flash('Posted', 'success')
        return redirect(url_for('pageBp.home'))
    else:
        return render_template('create_post.html', title='New Post', form=form, legend='New Post')
    
    
# give route to a specific post
@postBp.route('/post/<int:post_id>')
def post(post_id):
   post = Post.query.get_or_404(post_id)
   return render_template('post.html', title=post.title, post=post)


# update post
@postBp.route('/post/<int:post_id>/update', methods = ['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # only author can update
    if current_user != post.author:
        abort(403) 
    form = PostForm()
    # keep the content of origin post
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post Updated', 'success')
        return redirect(url_for('pageBp.home'))
    else:
        #if 
        form.title.data = post.title
        form.content.data = post.content
        return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')





@postBp.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', 'success')
    return redirect(url_for('pageBp.home'))