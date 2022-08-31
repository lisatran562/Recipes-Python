from flask_app import app, bcrypt
from flask import render_template, request, redirect, session, flash
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User

@app.route('/recipe/new')
def recipe_new():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('new_recipe.html')

@app.route('/create/recipe', methods = ['POST'])
def add_recipe():
    # validate new recipe
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    # create new data dict from request form for new recipe
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'under_thirty': request.form['under_thirty'],
        'user_id': session['user_id']
    }
    # save new recipe into database
    Recipe.create_recipe(data)
    return redirect('/dashboard')

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id': id
    }
    recipe_data = {
        'id': id
    }
    user = User.get_one(data)
    recipe = Recipe.get_one_recipe(recipe_data)
    return render_template('edit_recipe.html',user=user, recipe=recipe)

@app.route('/recipe/update/<int:id>', methods = ['POST'])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/edit/{id}') # NEED TO REDIRECT WITH AN F STRING TO RENDER PAGE CORRECTLY

    Recipe.edit_recipe(request.form)
    return redirect('/dashboard')

@app.route('/display/recipe/<int:id>')
def display_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    recipe_data = {
        'id': id
    }
    user = User.get_one(data)
    recipe = Recipe.get_one_recipe(recipe_data)
    return render_template('recipe.html', user=user, recipe=recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    data = {
        'id': id
    }

    Recipe.destroy(data)
    return redirect('/dashboard')


