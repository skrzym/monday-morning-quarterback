from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
def index2():
    return 'Admin'
