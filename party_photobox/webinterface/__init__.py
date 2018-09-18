from flask import Flask


app = Flask(__name__, static_folder = "../photo_folder")
app.config['SECRET_KEY'] = 'DuWeißtSchonWer'

from webinterface import routes
