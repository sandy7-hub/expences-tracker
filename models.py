from flask_sqlalchemy import SQLAlchemy
import models

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    username = db.Column(db.String(50),nullable = False)
    password = db.Column(db.String(250),nullable = False)

class Expenses (db.Model) :
    id = db.Column( db.Integer, primary_key = True , autoincrement = True )
    amount = db.Column(db.Float , nullable = False)
    category = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(50), nullable = False)
    date = db.Column(db.String(20), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    def __repr__(self):
        return f"<Expense {self.amount}>"

