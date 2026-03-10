from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import hashlib
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecret123'

USERS_FILE = 'users.json'
NOTATER_FILE = 'notater.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        save_users({})
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_notater():
    if not os.path.exists(NOTATER_FILE):
        return []
    with open(NOTATER_FILE, 'r') as f:
        return json.load(f)

def save_notater(notater):
    with open(NOTATER_FILE, 'w') as f:
        json.dump(notater, f, indent=2, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            flash('Du må logge inn for å se denne siden.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'username' not in session:
                flash('Du må logge inn for å se denne siden.', 'error')
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash(f'Tilgang nektet. Kun {", ".join(roles)} kan se denne siden.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/')
def index():
    USERS = load_users()
    if not USERS:
        return redirect(url_for('setup'))
    return redirect(url_for('dashboard') if 'username' in session else url_for('login'))

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    USERS = load_users()
    if USERS:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        name = request.form.get('name', '').strip()
        if username and password and name:
            USERS[username] = {
                'password': hash_password(password),
                'role': 'admin',
                'name': name
            }
            save_users(USERS)
            flash('Admin-konto opprettet! Logg inn.', 'success')
            return redirect(url_for('login'))
    return render_template('setup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        action = request.form.get('action')
        USERS = load_users()

        if action == 'login':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            user = USERS.get(username)
            if user and user['password'] == hash_password(password):
                session['username'] = username
                session['role'] = user['role']
                session['name'] = user['name']
                flash(f'Velkommen, {user["name"]}!', 'success')
                return redirect(url_for('dashboard'))
            flash('Feil brukernavn eller passord.', 'error')

        elif action == 'register':
            username = request.form.get('reg_username', '').strip()
            password = request.form.get('reg_password', '')
            name = request.form.get('reg_name', '').strip()
            if not username or not password or not name:
                flash('Alle felt må fylles ut.', 'error')
            elif username in USERS:
                flash(f'Brukernavnet "{username}" er allerede tatt.', 'error')
            else:
                USERS[username] = {
                    'password': hash_password(password),
                    'role': 'user',
                    'name': name
                }
                save_users(USERS)
                session['username'] = username
                session['role'] = 'user'
                session['name'] = name
                flash(f'Konto opprettet! Velkommen, {name}!', 'success')
                return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Du er nå logget ut.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/brukerpanel')
@role_required('admin', 'user')
def user_panel():
    return render_template('user_panel.html')

@app.route('/notattavle')
@login_required
def notattavle():
    return render_template('noteboard.html', notater=load_notater())

@app.route('/notattavle/legg-til', methods=['POST'])
@role_required('admin', 'user')
def legg_til_notat():
    tekst = request.form.get('tekst', '').strip()
    if tekst:
        notater = load_notater()
        notater.append({
            'tekst': tekst,
            'username': session['username'],
            'navn': session['name'],
            'rolle': session['role'],
        })
        save_notater(notater)
        flash('Notat lagt til!', 'success')
    return redirect(url_for('notattavle'))

@app.route('/notattavle/slett/<int:index>', methods=['POST'])
@login_required
def slett_notat(index):
    notater = load_notater()
    real_index = len(notater) - 1 - index
    if 0 <= real_index < len(notater):
        notat = notater[real_index]
        if session['role'] == 'admin' or session['username'] == notat['username']:
            notater.pop(real_index)
            save_notater(notater)
            flash('Notat slettet.', 'success')
        else:
            flash('Du kan bare slette dine egne notater.', 'error')
    return redirect(url_for('notattavle'))

@app.route('/admin')
@role_required('admin')
def admin_panel():
    USERS = load_users()
    return render_template('admin.html', users=USERS)

@app.route('/admin/endre/<username>', methods=['POST'])
@role_required('admin')
def endre_bruker(username):
    USERS = load_users()
    if username not in USERS:
        flash('Bruker ikke funnet.', 'error')
        return redirect(url_for('admin_panel'))
    if username == session['username']:
        flash('Du kan ikke endre din egen rolle.', 'error')
        return redirect(url_for('admin_panel'))

    ny_rolle = request.form.get('role')
    nytt_navn = request.form.get('name', '').strip()
    nytt_passord = request.form.get('password', '').strip()

    if nytt_navn:
        USERS[username]['name'] = nytt_navn
    if ny_rolle in ['guest', 'user', 'admin']:
        USERS[username]['role'] = ny_rolle
    if nytt_passord:
        USERS[username]['password'] = hash_password(nytt_passord)

    save_users(USERS)
    flash(f'Bruker "{username}" oppdatert.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/slett/<username>', methods=['POST'])
@role_required('admin')
def slett_bruker(username):
    USERS = load_users()
    if username == session['username']:
        flash('Du kan ikke slette deg selv.', 'error')
    elif username not in USERS:
        flash('Bruker ikke funnet.', 'error')
    else:
        del USERS[username]
        save_users(USERS)
        flash(f'Bruker "{username}" slettet.', 'success')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)