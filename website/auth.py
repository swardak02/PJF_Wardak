from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        uzytkownik = Uzytkownik.query.filter_by(email=email).first()
        if uzytkownik:
            if uzytkownik.password == password:
                flash('Logged in succesfully!', category='success')
                login_user(uzytkownik, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    return redirect(url_for('views.logout_strona'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        uzytkownik = Uzytkownik.query.filter_by(email=email).first()
        if uzytkownik:
            flash('Email already exists!', category='error')
        if len(email) < 4:
            flash('Email must be greater than 4 characters!', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters!', category='error')
        elif len(lastName) < 2:
            flash('Last name must be greater than 2 characters!', category='error')
        elif password1 != password2:
            flash('Your passwords dont match!', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters!', category='error')
        else:
            new_user = Uzytkownik(email=email, firstName=firstName, lastName=lastName,
                                  password=password1, stanowisko="Użytkownik")
            db.session.add(new_user)
            db.session.commit()
            login_user(uzytkownik, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/oferty')
@login_required
def oferty():
    oferty_pracy = Oferta.query.all()
    return render_template("oferty.html", user=current_user, oferty_pracy=oferty_pracy)