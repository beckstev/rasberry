import flask
from webinterface import app
from flask_socketio import SocketIO
import threading
import numpy as np

socketio = SocketIO(app)


@app.before_first_request
def init_app():
    start_image_updater()


def start_image_updater():
     t = threading.Timer(1, start_image_updater)
     t.daemon = True
     t.start()

     photo_number = np.genfromtxt( './photo_folder/filenumber.txt', unpack = True)
     print('Updated image', photo_number)

     image_name = "{{ url_for('static', filename=image_" + str(int(photo_number)) + ".jpg) }}"

     socket.emit('update', image_name)





# Update Website
socketio.on('update')
def handle_message(photo_number):
    image_name = 'image_'+ photo_number + '.jpg'
    return flask.render_template('show_picture.html', image_name = image_name)


### Init socket
socket = SocketIO()
socket.init_app(app)


@app.route('/')
def test():
    image_name = 'image_'+ '1' + '.jpg'
    return flask.render_template('show_picture.html', image_name = image_name)


@app.route('/test')
def test_2():
    return 'Geklappt'
