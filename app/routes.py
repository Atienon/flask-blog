from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import LoginDashboardForm, NewPostForm
from app.models import User, Post
from app import app, db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginDashboardForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin'))
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login_dashboard.html', title='Dashboard Login', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, description=form.description.data,
            body=form.body.data)
        db.session.add(new_post)
        db.session.commit()
        flask("New post has been posted")
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', title='Dashboard', form=form)

@app.route('/all_posts')
@login_required
def all_posts():
    return render_template('all_posts.html', title='All posts')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
