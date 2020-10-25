from flask import render_template, url_for, flash, redirect, request, Blueprint
from forumFlask import db, bcrypt
from forumFlask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from forumFlask.user.form import RegistrationForm, LoginForm, AccountForm, ResetPassRequestForm, ResetPassForm
from forumFlask.user.util import savePic, sendEmail




userBp = Blueprint('userBp', __name__)


@userBp.route('/login', methods=['GET','POST'])
def login():
    #if logged in, then redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('pageBp.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        #query db for user
        user = User.query.filter_by(email=form.email.data).first()
        #user exist and password match
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #log in 
            login_user(user, remember=form.remember.data)
            flash(f'Login successful', 'success')
            #access the page intended before login
            #  http://localhost:5000/login?next=%2Fhome
            #   args is a dict 
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('pageBp.home'))
        else:
            flash(f'Please enter valid email&password', 'danger')
            
    return render_template('login.html', title='Log in', form = form)

@userBp.route('/register', methods = ['GET', 'POST'])
def register():
    #if logged in, then redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('pageBp.home'))
    
    form = RegistrationForm()
    #if request.method = 'POST' and form.validate()
    if form.validate_on_submit():
        #hash the password
        hashPw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #create new user
        newUser = User(username=form.username.data, email=form.email.data, password=hashPw)
        #add user to db
        db.session.add(newUser)
        db.session.commit()
        #flash msg
        flash(f'New acount created for {form.username.data}', 'success')
        #home here is the view function name
        return redirect(url_for('pageBp.home'))
    else:
        return render_template('register.html', title='Register', form = form)
    
    
@userBp.route('/account', methods = ['POST', 'GET'])
@login_required
def account():
    img = url_for('static', filename='pics/' + current_user.img_file)
    form = AccountForm()
    #update
    if form.validate_on_submit():
        #if uploaded a pic
        if form.img.data:
            f_name = savePic(form.img.data)
            current_user.img_file = f_name
        current_user.username = form.username.data
        db.session.commit()
        flash('Account updated!', 'success')
        # post-get-redirect pattern
        return redirect(url_for('userBp.account'))
    else:
        return render_template('account.html', title='Account', img=img, form=form)
    


#route for specific user and his posts
@userBp.route('/user/<string:username>')
def user_post(username):
    # get the page number in url to get the specific page (default 1)
    #pageN = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # use sqlAlchemy to paginate posts   order the post to latest at top   set page size to 6     
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(per_page=6)
    
    return render_template('user_post.html', post=posts, user=user)


@userBp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('userBp.login'))


# request pw reset
@userBp.route('/reset_req', methods = ['POST', 'GET'])
def reset_req():
    form = ResetPassRequestForm()
    if form.validate_on_submit():
        # get user and send user an email with token
        user = User.query.filter_by(email=form.email.data).first()
        sendEmail(user)
        flash('Email Sent!', 'info')
        return redirect(url_for('pageBp.home'))
    else:
        return render_template('requestPw.html', title='Reset Password', form=form)
    
    
# reset pw
# <> means parameter
@userBp.route('/reset_pw/<token>', methods = ['POST', 'GET'])
def reset(token):
    # verify the token
    user = User.verify_token(token)
    if not user:
        flash('Invalid ot expired token', 'warning')
        return redirect(url_for('userBp.reset_req'))
    
    form = ResetPassForm()
    if form.validate_on_submit():
        hashPw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashPw
        db.session.commit()
        flash('Password Updated!', 'success')
        return redirect(url_for('userBp.login'))
    else:
        return render_template('resetPw.html', title='Reset Password', form=form)