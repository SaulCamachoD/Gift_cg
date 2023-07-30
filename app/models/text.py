from app.config.mysqlconnection import connectToMySQL
from flask import flash

class Text:
    db_name = 'gift_cg'
    def init(self, data):
        self.id = data["id"]
        self.letter = data["letter"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def save_letter(cls, data):
        query = "INSERT INTO ms (letter, user_id) VALUES (%(letter)s,%(id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results   

    @classmethod
    def get_letter(cls, data):
        query = "SELECT ms.letter FROM ms where id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results      