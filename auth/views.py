from flask import render_template,  redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from models.extensions import db, User
from flask_login import login_user, login_required, logout_user
from sqlalchemy import exc


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    """Register form"""

    email = StringField('Email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])


def authenticate():
    """Login route"""

    form = LoginForm()

    if form.validate_on_submit():
        # Find the user with the username provided
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Test that the password matches the password in database
            if check_password_hash(user.password, form.password.data):
                # Ensure sufficient permissions
                if(user.perms):
                    # Login user
                    login_user(user, remember=form.remember.data)
                    # Redirect if next parameter is passed
                    nurl = request.form.get("next")
                    if nurl:
                        return redirect(nurl)
                    else:
                        return redirect('/')
                else:
                    # User did not have sufficient permissions, display error message
                    if(user.checked):
                        return render_template('/auth/auth.html', form=form, lg="Your account was not verified. Please contact an administrator for further inquiries.")
                    else:
                        return render_template('/auth/auth.html', form=form, lg="Your account is still being verified. Please try again later!")
        # Either incorrect password or username was not in database
        return render_template('/auth/auth.html', form=form, lg="Incorrect username or password")
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('/auth/auth.html', form=form)


def register():
    """Register route"""

    form = RegisterForm()

    if form.validate_on_submit():
        # Generate hash of password provided
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        # Create new unchecked user with given username, password and email, set to default permissions
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, perms=0, checked=False)

        db.session.add(new_user)

        try:
            db.session.commit()
        except exc.IntegrityError:
            # Failed unique constraint - username/email already in database
            return render_template('/auth/Nauth.html', form=form, lg="This email/username is already taken.")
        return redirect('/authenticate')
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('/auth/Nauth.html', form=form)


@login_required
def endsession():
    """Logout route"""

    logout_user()
    return redirect('/')
