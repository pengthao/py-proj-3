'''
set FLASK_APP=app.py    
flask --app app.py db init
flask --app app.py db migrate -m "initial migration"
flask --app app.py db upgrade
'''

from myproject import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationFrom
from flask_dance.contrib.google import make_google_blueprint, google

blueprint = make_google_blueprint(client_id='', client_secret='',
                                    offline=True, scope=['profile', 'email'])

app.register_blueprint(blueprint, url_prefix='/login')

app.app_context().push()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            
            login_user(user)
            flash('Logged in Successfully!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('welcome_user')

            return redirect(next)
    
    return render_template('login.html', form=form)

@app.route('/login/google')
def login_g():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']

    return render_template('welcome_user.html', email=email)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationFrom()

    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


if __name__=='__main__':
    app.run(debug=True)