from flask import Blueprint, render_template

errorBp = Blueprint('errorBp', __name__)

# app_errorhandler will work for whole application instead of single bp
@errorBp.app_errorhandler(404)
def error_404(error):
        return render_template('errors/404.html'), 404
    
    
@errorBp.app_errorhandler(403)
def error_403(error):
        return render_template('errors/403.html'), 403
    
    
@errorBp.app_errorhandler(500)
def error_500(error):
        return render_template('errors/500.html'), 500