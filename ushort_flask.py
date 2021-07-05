import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Datarequired
from flask import url_for
from flask import render_template
import ushort


# export FLASK_APP=ushort_flask.py
# flask run or python3 -m flask ushort_flask
app = Flask(__name__)
app.secret_key = os.urandom(32).decode('utf-8', errors='ignore')

class URL_Form(FlaskForm):
    urlname = StringField('url_name', validators=[Datarequired()])
    submit = SubmitField('Shorten')

@app.route('/')
def index():
    form = URL_Form()
    if form.validate_on_submit():
        print(f'{form.urlname.data}')
        redirect('success') 
    return render_template('base.html', form=form)

@app.route('/success'):
    render_template('success.html')
with app.test_request_context():
    print(url_for('index'))
    print(url_for('success'))


if __name__ == '__main__':
	app.run()
