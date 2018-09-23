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
    #Update
     t = threading.Timer(0.01, start_image_updater)
     t.daemon = True
     t.start()
     #Get the number of the newest photo
     photo_number = np.genfromtxt( './photo_folder/filenumber.txt', unpack = True)
     # Generate the name for the html template. I was not sure how to use a variable in "url_for", so I trie this as workaround
     pic_name = "/photo_folder/image_" + str(int(photo_number)) + ".jpg"
     emit_var = [ 'Bildnummer: ' + str(int(photo_number)), pic_name ]
     #Emit Update command

     socket.emit('update', emit_var)
     #socket.emit('title_update', str(int(photo_number)))



### Init socket
socket = SocketIO()
socket.init_app(app)


# The first apparance of the website is defined here. So it should show at the beginning the image with number 1
@app.route('/')
def test():
    image_name = 'image_1.jpg'
    image_number = '1'
    return flask.render_template('show_picture.html', image_name = image_name, image_number = image_number)

# Just a test function
@app.route('/test')
def test_2():
    return 'Geklappt'
