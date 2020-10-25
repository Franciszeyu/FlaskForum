import os 

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    #/// means relative location to the current file
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # use env car to store sensitive info
    MAIL_USERNAME = os.environ["USER_NAME"]
    MAIL_PASSWORD = os.environ["USER_PASS"]
    