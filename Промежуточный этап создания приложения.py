from flask import render_template, Flask
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from data.jobs import Jobs

from forms.login_form import LoginForm
from forms.new_jobs_form import NewJobForm
from forms.reg_form import RegisterForm

db_session.global_init('db/blogs.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def func():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        jobs = current_user.jobs
    else:
        jobs = db_sess.query(Jobs).all()
    return render_template('start.html', current_user=current_user, jobs=jobs, len_jobs=len(jobs))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def new_job():
    form = NewJobForm()
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.jobs.data
        job.collaborators = form.collaborators.data
        job.work_size = form.size.data
        job.is_finished = form.finish.data
        job.team_leader = form.lead.data
        if job and form.submit:
            db_sess = db_session.create_session()
            db_sess.add(job)
            db_sess.commit()
            # login_user(user, remember=form.remember_me.data)

            return redirect("/")
        return render_template('new_job.html',
                               message="Введите еще раз",
                               form=form, simple=False)
    return render_template('new_job.html', form=form, simple=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
            )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
