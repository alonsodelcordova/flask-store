from flask import request, make_response, redirect, render_template, session, url_for
from flask import Blueprint, flash
from apps.forms.login_form import LoginForm

tp_route = Blueprint(
    url_prefix='',
    name='Templates',
    import_name=__name__,
)


@tp_route.get('/')
def inicio():
    user_ip = request.remote_addr
    session['user_ip'] = user_ip
    response = make_response(redirect('/hello'))
    return response


@tp_route.get('/hello')
def hello():
    todos = [
        {'id': 1, 'name': 'Juan'},
        {'id': 2, 'name': 'Carmen'},
        {'id': 3, 'name': 'Rosita'},
        {'id': 4, 'name': 'Carlos'},
    ]
    ip = session.get('user_ip')
    context = {
        'ip': ip,
        'todos': todos,
    }
    return render_template('index.html', **context)

@tp_route.get('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@tp_route.get('/login')
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render_template('login.html', **context)

@tp_route.post('/login')
def login_post():
    login_form = LoginForm(request.form)

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Usuario registrado con éxito')
        return redirect(url_for('Templates.hello'))
    print('No validado')
    context = {
        'login_form': login_form,
    }
    return render_template('login.html', **context)

@tp_route.get('/logout')
def logout():
    if 'username' in session:
        flash(f'Usuario {session["username"]} ha cerrado sesión', 'info')
        session.pop('username')
    return redirect(url_for('Templates.login'))