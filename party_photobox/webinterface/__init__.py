from flask import Flask


app = Flask(__name__, static_folder = "../photo_folder")

from webinterface import routes