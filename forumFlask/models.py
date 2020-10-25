from datetime import datetime
from forumFlask import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#create classes --- tables for db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #uset to post 1--many  backref declares a new property（not column） on the post table but not in user table
    #but a post.author will return a whole user object
    #user.posts return list of post objects
    posts = db.relationship('Post', backref='author', lazy=True)

    #method easier to create tokens
    #JSON Web Signature (JWS)
    def get_reset_token(self, expires_sec=1800):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_sec)  
        return s.dumps({'user_id':self.id}).decode('utf-8')
          
    # method to verify the token
    @staticmethod
    def verify_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            # return will be a dict
            user_id = s.loads(token)['user_id']
        except:
            return None
        #return the user with that id
        return User.query.get(user_id)

    def __repr__(self):        
        return f"User('{self.username}', '{self.email}', '{self.img_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
                                            #don't put utcnow() cuz that will call and set all the time to now
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"


