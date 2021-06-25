from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from todolist.forms import LoginForm, RegistrationForm, TaskForm
from todolist.model import User, Task
from todolist import app, db, bcrypt

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home')

@app.route('/about')
def about():
	return render_template('about.html', title='Home')

@app.route('/list', methods=['GET', 'POST'])
@login_required
def todolist():
	form = TaskForm()
	if form.validate_on_submit():
		task = Task(title=form.title.data, author=current_user)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('todolist'))
	if current_user.is_authenticated:
		user = User.query.filter_by(username=current_user.username).first_or_404()
		tasks = Task.query.filter_by(author=user)
		return render_template('list.html', title='Home', tasks=tasks, form=form)
	else:
		return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        # else:
            # flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/task/<int:task_id>/delete")
@login_required
def task_delete(task_id):
	task = Task.query.get_or_404(task_id)
	if task.author != current_user:
		abort(403)
	db.session.delete(task)
	db.session.commit()
	return redirect(url_for('todolist'))

@app.route("/task/<int:task_id>/info", methods=['POST', 'GET'])
@login_required
def task_info(task_id):
	task = Task.query.get_or_404(task_id)
	if task.author != current_user:
		abort(403)
	if request.method == "POST":
		task.title = request.form['title']
		task.description = request.form['description']
		db.session.commit()
		return redirect(url_for('todolist'))
	return render_template('task_info.html', task = task)


@app.route("/task/<int:task_id>/check", methods=['POST', 'GET'])
@login_required
def task_check(task_id):
	task = Task.query.get_or_404(task_id)
	if task.author != current_user:
		abort(403)
	task.checked = not task.checked
	db.session.commit()
	return redirect(url_for('todolist'))