from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegistrationForm, CommentForm
from app.models import User, Post, Comment


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    sort_by = request.form.get('sort_by')

    posts = Post.query.order_by(Post.timestamp.asc()).all()
    if sort_by == 'descending':
        posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def detail(post_id):
    form = CommentForm()
    if request.method == 'POST':
        comment = Comment(value=form.value.data, post_id=post_id, user_id=current_user.get_id())
        db.session.add(comment)
        db.session.commit()

    post = Post.query.filter_by(id=post_id).first()
    post_comments = Comment.query.filter_by(post_id=post_id).all()

    return render_template('detail.html', title='Post Detail', post=post, form=form, postComments=post_comments)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
