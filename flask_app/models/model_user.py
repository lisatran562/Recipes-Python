from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_reg(data):
        is_valid = True

        if len(data['first_name']) < 2:            
            is_valid = False
            flash('First name must be at least 2 characters', 'err_user_reg_first_name')

        if len(data['last_name']) < 2:
            is_valid = False
            flash('Last name must have at least 2 characters', 'err_user_reg_last_name')

        if len(data['email']) < 1:
            is_valid = False
            flash('Must have an email', 'err_user_reg_email')

        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Invalid email', 'err_user_reg_email')
        
        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if potential_user:
                is_valid = False
                flash('Email already exists', 'err_user_reg_email')

        if len(data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters', 'err_user_reg_pw')

        if len(data['confirm_pw']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters', 'err_user_reg_confirm_pw')

        elif data['password'] != data['confirm_pw']:
            is_valid = False
            flash('Passwords must match', 'err_user_reg_confirm_pw')
        
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True

        if len(data['email']) < 1:
            is_valid = False
            flash('Please enter your email', 'err_user_login_email')

        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Invalid email', 'err_user_login_email')

        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if not potential_user:
                is_valid = False
                flash('Email does not exist', 'err_user_login_email')
            else:
                if not bcrypt.check_password_hash(potential_user.password, data['password']):
                    is_valid = False
                    flash('Password not correct', 'err_user_login_pw')
                else:
                    session['user_id'] = potential_user.id
        if len(data['password']) < 1:
            is_valid = False
            flash('Please enter your password', 'err_user_login_pw')
            
        return is_valid


