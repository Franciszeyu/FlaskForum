import secrets
import os
from PIL import Image
from forumFlask import mail 
from flask_mail import Message
from flask import url_for, current_app


def savePic(pic):
    #use random hex for file name
    rand = secrets.token_hex(8)
    #save the file ext
    _, f_ext = os.path.splitext(pic.filename)
    f_name = rand + f_ext
    #path
    pathP = os.path.join(current_app.root_path, 'static/pics', f_name)
    #resize image that is too large to save space
    outSize = (125, 125)
    newImage = Image.open(pic)
    newImage.thumbnail(outSize)
    #save
    newImage.save(pathP)
    
    return f_name



#send email
def sendEmail(user):
    #get the token
    token = user.get_reset_token()
    msg = Message("Password Reset",
                  sender=os.environ["USER_NAME"],
                  recipients=[user.email])
    msg.body = f'''Click link below:
                        {url_for('userBp.reset', token=token, _external=True)}
                    If you didn't request this change, ignore this email and check your account.'''  #external to get absolute url
    
    mail.send(msg)