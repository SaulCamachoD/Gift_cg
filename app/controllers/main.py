from flask import render_template, request, redirect, session, flash
from app import app
from app.models.user import User
from app.models.text import Text
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/presentation')
def presentation():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
    }
    user = User.get_only_name(data)
    nombre = user[0]['name']

    return render_template('presentation.html', user=nombre)


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    else:
        data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password']),
            "explanation": request.form['explanation'],

        }
        User.save(data)
        return redirect('/presentation')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_name(request.form)
    if not user:
        flash("Nombre incorrecto", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(
            "Compañia equivocada !Recuerda el lugar donde trabajaste en Guaymaral!", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/presentation')


@app.route('/acertijo_1/000/ac1')
def retoa():
    return render_template('acertijo_1.html')


@app.route('/acertijo_1/11449/ac1')
def retob():
    return render_template('acertijo_2.html')


@app.route('/check_number', methods=['POST'])
def check_number():
    number = request.form['number']
    if number == '68':
        return redirect('/acertijo_3')
    else:
        return redirect('/acertijo_1/11449/ac1')


@app.route('/check_hechizo', methods=['POST'])
def check_hechizo():
    number = request.form['hechizo']
    if number == 'sectumsempra':
        return redirect('/clave')
    else:
        return redirect('/acertijo_3')


@app.route('/acertijo_3')
def retoc():
    return render_template('acertijo_3.html')


@app.route('/clave')
def clave():
    return render_template('clave.html')


@app.route('/eleccion')
def eleccion():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
    }
    user = User.get_only_name(data)
    exp = User.get_only_expl(data)
    nombre = user[0]['name']
    explicacion = exp[0]['explanation']
    return render_template('eleccion.html', user=nombre, explicacion=explicacion)


@app.route('/texto')
def txt():
    return render_template('texto.html')


@app.route('/text_c', methods=['POST'])
def txtc():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
        "letter": request.form['letter']
    }
    Text.save_letter(data)
    return redirect('/eleccion')


@app.route('/final')
def end():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
    }
    desc = Text.get_letter(data)
    descripcion = desc[0]['letter']
    return render_template('end.html', descripcion=descripcion)
