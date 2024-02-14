from flask import Blueprint, render_template, redirect, request, url_for, flash 
from project.models import User, get_by_username, customers
from project.users.forms import LoginForm,RegistrationForm
from flask_login import login_user, login_required, logout_user

users_blueprint = Blueprint('users', __name__, template_folder='templates/users')

@users_blueprint.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))

@users_blueprint.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = get_by_username(form.username.data)
        

        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Logged in Successfully!')

                next = request.args.get('next')

                if next == None or not next[0] == '/':
                    next = url_for('users.welcome_user')

                return redirect(next)
    
    return render_template('login.html', form=form)

@users_blueprint.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        RegistrationForm.check_username(form.username.data)

        user = User(username = form.username.data,
                    password = form.password.data,
                    name = form.name.data)
        
        customers[user.username] = user.to_dict()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)