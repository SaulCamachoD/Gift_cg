from flask import flash
from app.config.mysqlconnection import connectToMySQL
import re
from app import app
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db_name = 'gift_cg'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.explanation = data['explanation']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name,email,password,explanation,created_at,updated_at) VALUES(%(name)s,%(email)s,%(password)s,%(explanation)s,NOW(),NOW());"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_by_name(cls, data):
        query = "SELECT * FROM users WHERE name = %(name)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_only_expl(cls, data):
        query = "SELECT explanation FROM users where id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_only_name(cls, data):
        query = "SELECT name FROM users where id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, user)
        if len(user['name']) < 3:
            flash("Name must be at least 3 characters", "register")
            is_valid = False
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
        if len(user['explanation']) == 0:
            flash("Please write anything in word", "register")
            is_valid = False
        return is_valid
