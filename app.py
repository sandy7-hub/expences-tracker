
from flask import Flask, render_template, redirect,request,session,url_for
from models import db, Expenses, User 
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key = "secret"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app,db)

with app.app_context():
    db.create_all()




@app.route('/', methods=['GET', 'POST'])
def register():

    if request.method != 'POST':
        return render_template('register.html')
    username = request.form['username']
    password = generate_password_hash(request.form['password'])

    if existing_user := User.query.filter_by(username=username).first():
        return "Username already exists "

    user = User(username=username, password=password)

    db.session.add(user)
    db.session.commit()

    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method != 'POST':
        return render_template('login.html')
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    if not username or not password:
        return redirect('/logout')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return redirect('/logout')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')
        





@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        data = request.form
        new_expense = Expenses(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date=data['date'],
            user_id=session['user_id']
        )
        db.session.add(new_expense)
        db.session.commit()

    expenses = Expenses.query.filter_by(user_id=session['user_id']) .all()

    total = sum(int(exp.amount) for exp in expenses)
    if total > 5000:
        
        message = "You are spending too much!"
    else:
        message = "Spending looks good!"

    return render_template('home.html', expenses=expenses, total=total, message=message)

@app.route('/delete/<int:id>')
def delete(id):
    exp = Expenses.query.get(id)
    db.session.delete(exp)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/edit/<int:id>' , methods = ['GET' , 'POST'])
def edit(id) :
    exp = Expenses.query.get(id)
    
    if request.method == 'POST' :
        exp.amount = request.form['amount']
        exp.category = request.form['category']
        exp.description = request.form['description']
        exp.date = request.form['date']
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit.html' , expense = exp)
        






