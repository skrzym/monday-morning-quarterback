from flask import Flask
from mmq.main.controllers import main
from mmq.admin.controllers import admin
from config import mongo


app = Flask(__name__, template_folder='templates')
app.config.from_object('config.DevelopmentConfig')
mongo.init_app(app)

#app.register_blueprint(main, url_prefix='/')
#app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(main)
app.register_blueprint(admin)
