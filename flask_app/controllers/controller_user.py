from flask_app import app, bcrypt
from flask import render_template, request, redirect, session
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe


@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_reg(request.form):
        return redirect('/')

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }

    id = User.create(data)

    session['user_id'] = id    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }

    if not User.validate_login(request.form):
        return redirect('/')

    user = User.get_one_by_email(data)

    if not bcrypt.check_password_hash(user.password,request.form['password']):
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id': session['user_id']
    }
    print(data)
    user = User.get_one(data)
    recipes = Recipe.get_all_recipes_with_users()
    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route('/logout')
def logout():
    del session['user_id']

    return redirect('/')

