from flask import Flask
from mmq.main.controllers import main
from mmq.admin.controllers import admin
<<<<<<< HEAD
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
=======
>>>>>>> master
from config import mongo


app = Flask(__name__, template_folder='templates')
app.config.from_object('config.DevelopmentConfig')
<<<<<<< HEAD
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3000 per hour","5 per 1 seconds"]
)
=======
>>>>>>> master
mongo.init_app(app)

#app.register_blueprint(main, url_prefix='/')
#app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(main)
app.register_blueprint(admin)
