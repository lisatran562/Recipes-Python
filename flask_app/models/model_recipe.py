from sqlite3 import connect
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask_app.models import model_user

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_thirty = data['under_thirty']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under_thirty, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_thirty)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, under_thirty = %(under_thirty)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_all_recipes_with_users(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(DB).query_db(query)
        if results:
            list_of_recipes = []
            # loop through the list of dictionaries
            for recipe_dictionary_with_one_user in results:
                # {}
                print(recipe_dictionary_with_one_user)
                # creating a recipe instance
                recipe = cls(recipe_dictionary_with_one_user)
                # creating a user dictionary 
                user_dictionary = {
                    'id': recipe_dictionary_with_one_user['users.id'],
                    'first_name': recipe_dictionary_with_one_user['first_name'],
                    'last_name': recipe_dictionary_with_one_user['last_name'],
                    'email': recipe_dictionary_with_one_user['email'],
                    'password': recipe_dictionary_with_one_user['password'],
                    'created_at': recipe_dictionary_with_one_user['users.created_at'],
                    'updated_at': recipe_dictionary_with_one_user['users.updated_at']
                }
                # creating a user instance
                user = model_user.User(user_dictionary)
                # adding user attributes to recipe instance
                recipe.user = user
                list_of_recipes.append(recipe)
                print(list_of_recipes)
            return list_of_recipes
        return False

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3:
            is_valid = False
            flash('Name must be at least 3 characters', 'err_recipe_name')

        if len(data['description']) < 3:
            is_valid = False
            flash('Description must be at least 3 characters', 'err_recipe_description')

        if len(data['instructions']) < 3:
            is_valid = False
            flash('Instructions must be at least 3 characters', 'err_recipe_instructions')
        
        if len(data['date']) < 1:
            is_valid = False
            flash('Please enter date made', 'err_recipe_date')

        if 'under_thirty' not in data:
            is_valid = False
            flash('Please specify if recipe can be made under 30 minutes', 'err_recipe_under_thirty')

        return is_valid

