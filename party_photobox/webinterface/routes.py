import flask
from webinterface import app
image_name = 'image_1.jpg'
image_number = 1
width = 4000
height =  3000
name_url = "localhost:5000/" + str(image_number+1)
@app.route('/')
def test():
    return flask.render_template('show_picture.html', image_name = image_name, name_url = name_url)


@app.route('/test')
def test_2():
    return 'Geklappt'

@app.route(f'/' + str(image_number+1))
def show_picture(image_number):
    try:
        print('im Try')
        image_number +=1
        image_name = 'image_' + str(image_number) + '.jpg'
        name_url = "2; URL=localhost:5000/" + str(image_number)
        return flask.render_template('show_picture.html', image_name = image_name, name_url = name_url )
    except:
        print('im except')
        image_name = 'image_' + str(image_number) + '.jpg'
        name_url ="2; URL=localhost:5000/" + str(image_number)
        return flask.render_template('show_picture.html', image_name = image_name, name_url = name_url)
