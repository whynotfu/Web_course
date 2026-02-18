import re
import sqlite3
from datetime import datetime
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_login import (LoginManager, UserMixin, login_user,
                         logout_user, login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'lb4-secret-key-change-in-production'
application = app

DATABASE = 'users.db'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо войти.'
login_manager.login_message_category = 'warning'


# ── DB helpers ──────────────────────────────────────────────────────────────

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS roles (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                description TEXT
            );
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                login         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                last_name     TEXT,
                first_name    TEXT NOT NULL,
                middle_name   TEXT,
                role_id       INTEGER REFERENCES roles(id),
                created_at    TEXT NOT NULL
            );
        ''')
        if not db.execute('SELECT 1 FROM roles LIMIT 1').fetchone():
            db.execute("INSERT INTO roles (name, description) VALUES ('admin', 'Администратор')")
            db.execute("INSERT INTO roles (name, description) VALUES ('user',  'Пользователь')")
        if not db.execute('SELECT 1 FROM users LIMIT 1').fetchone():
            db.execute(
                'INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id, created_at)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                ('admin', generate_password_hash('Admin123!'),
                 'Иванов', 'Иван', 'Иванович', 1, datetime.now().isoformat())
            )
        db.commit()


# ── User model ───────────────────────────────────────────────────────────────

class User(UserMixin):
    def __init__(self, id, login, password_hash, last_name, first_name,
                 middle_name, role_id, created_at):
        self.id = id
        self.login = login
        self.password_hash = password_hash
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.role_id = role_id
        self.created_at = created_at


@login_manager.user_loader
def load_user(user_id):
    row = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return User(**dict(row)) if row else None


# ── Jinja2 helper ────────────────────────────────────────────────────────────

@app.template_global()
def full_name(last, first, middle):
    return ' '.join(p for p in [last, first, middle] if p)


# ── Validation ───────────────────────────────────────────────────────────────

def validate_login(value):
    if not value:
        return 'Поле не может быть пустым.'
    if len(value) < 5:
        return 'Логин должен содержать не менее 5 символов.'
    if not re.fullmatch(r'[a-zA-Z0-9]+', value):
        return 'Логин должен состоять только из латинских букв и цифр.'
    return None


def validate_password(value):
    if not value:
        return 'Поле не может быть пустым.'
    if len(value) < 8:
        return 'Пароль должен содержать не менее 8 символов.'
    if len(value) > 128:
        return 'Пароль не должен превышать 128 символов.'
    if ' ' in value:
        return 'Пароль не должен содержать пробелы.'
    if not re.search(r'[A-ZА-ЯЁ]', value):
        return 'Пароль должен содержать хотя бы одну заглавную букву.'
    if not re.search(r'[a-zа-яё]', value):
        return 'Пароль должен содержать хотя бы одну строчную букву.'
    if not re.search(r'[0-9]', value):
        return 'Пароль должен содержать хотя бы одну цифру.'
    allowed = r"^[a-zA-Zа-яА-ЯёЁ0-9~!?@#$%^&*_\-+()\[\]{}<>/\\|\"'.,;:]+$"
    if not re.match(allowed, value):
        return 'Пароль содержит недопустимые символы.'
    return None


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    users = get_db().execute('''
        SELECT u.*, r.name AS role_name
        FROM users u LEFT JOIN roles r ON u.role_id = r.id
        ORDER BY u.id
    ''').fetchall()
    return render_template('index.html', title='Пользователи', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        login_val = request.form.get('login', '').strip()
        password  = request.form.get('password', '')
        remember  = bool(request.form.get('remember'))
        row = get_db().execute('SELECT * FROM users WHERE login = ?', (login_val,)).fetchone()
        if row and check_password_hash(row['password_hash'], password):
            login_user(User(**dict(row)), remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            next_page = request.args.get('next', '')
            if next_page and urlparse(next_page).netloc == '':
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('Неверный логин или пароль.', 'danger')
    return render_template('login.html', title='Вход')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>')
def user_view(user_id):
    row = get_db().execute('''
        SELECT u.*, r.name AS role_name
        FROM users u LEFT JOIN roles r ON u.role_id = r.id
        WHERE u.id = ?
    ''', (user_id,)).fetchone()
    if row is None:
        flash('Пользователь не найден.', 'danger')
        return redirect(url_for('index'))
    return render_template('user_view.html', title='Просмотр пользователя', user=row)


@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def user_create():
    db = get_db()
    roles = db.execute('SELECT * FROM roles').fetchall()
    errors = {}
    form_data = {}

    if request.method == 'POST':
        form_data = {k: v.strip() for k, v in request.form.items()}
        errors['login']      = validate_login(form_data.get('login', ''))
        errors['password']   = validate_password(form_data.get('password', ''))
        if not form_data.get('last_name'):
            errors['last_name'] = 'Поле не может быть пустым.'
        if not form_data.get('first_name'):
            errors['first_name'] = 'Поле не может быть пустым.'
        errors = {k: v for k, v in errors.items() if v}

        if not errors:
            try:
                db.execute(
                    'INSERT INTO users (login, password_hash, last_name, first_name,'
                    ' middle_name, role_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (
                        form_data['login'],
                        generate_password_hash(form_data['password']),
                        form_data.get('last_name') or None,
                        form_data['first_name'],
                        form_data.get('middle_name') or None,
                        form_data.get('role_id') or None,
                        datetime.now().isoformat(),
                    )
                )
                db.commit()
                flash('Пользователь успешно создан.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Ошибка при создании пользователя: {e}', 'danger')

    return render_template('user_form.html', title='Создание пользователя',
                           roles=roles, errors=errors, form_data=form_data, is_edit=False)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    db = get_db()
    row = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if row is None:
        flash('Пользователь не найден.', 'danger')
        return redirect(url_for('index'))
    roles = db.execute('SELECT * FROM roles').fetchall()
    errors = {}
    form_data = dict(row)

    if request.method == 'POST':
        form_data = {k: v.strip() for k, v in request.form.items()}
        if not form_data.get('last_name'):
            errors['last_name'] = 'Поле не может быть пустым.'
        if not form_data.get('first_name'):
            errors['first_name'] = 'Поле не может быть пустым.'

        if not errors:
            try:
                db.execute(
                    'UPDATE users SET last_name=?, first_name=?, middle_name=?, role_id=? WHERE id=?',
                    (
                        form_data.get('last_name') or None,
                        form_data['first_name'],
                        form_data.get('middle_name') or None,
                        form_data.get('role_id') or None,
                        user_id,
                    )
                )
                db.commit()
                flash('Данные пользователя успешно обновлены.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Ошибка при обновлении: {e}', 'danger')

    return render_template('user_form.html', title='Редактирование пользователя',
                           roles=roles, errors=errors, form_data=form_data,
                           is_edit=True, user_id=user_id)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def user_delete(user_id):
    db = get_db()
    try:
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()
        flash('Пользователь успешно удалён.', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении: {e}', 'danger')
    return redirect(url_for('index'))


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    errors = {}
    if request.method == 'POST':
        old_password     = request.form.get('old_password', '')
        new_password     = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not check_password_hash(current_user.password_hash, old_password):
            errors['old_password'] = 'Неверный текущий пароль.'
        err = validate_password(new_password)
        if err:
            errors['new_password'] = err
        if new_password and new_password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают.'

        if not errors:
            try:
                db = get_db()
                db.execute('UPDATE users SET password_hash=? WHERE id=?',
                           (generate_password_hash(new_password), current_user.id))
                db.commit()
                flash('Пароль успешно изменён.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Ошибка при смене пароля: {e}', 'danger')

    return render_template('change_password.html', title='Изменение пароля', errors=errors)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
