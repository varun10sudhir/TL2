from flask import Flask,render_template,redirect,url_for,request
import flask_login
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm,LoginForm
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required,current_user

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = 'aaccfca992d31f414ef45d0f'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key = True)
    Name = db.Column(db.String(length=30),nullable = False,unique = True)
    password = db.Column(db.String(length=60),nullable=False)
    score = db.Column(db.Integer(),nullable=False,default=0)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/quiz",methods = ['GET','POST'])
@login_required
def quizhtml():
    score=0
    cuser = User.query.filter_by(Name = current_user.Name).first()
    if request.method == 'POST':
        score = request.form['submit']
        cuser.score = score
        db.session.commit()
        print("Updated")
        return redirect(url_for('scoreboard'))
    return render_template('quiz.html')

@app.route("/signup",methods = ['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(Name=form.name.data,password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        return redirect(url_for('quizhtml'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            print(f'There was an error in the message{err_msg}')
    return render_template('signup.html',form=form)

@app.route("/login",methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(Name = form.name.data).first()
        if attempted_user:
            if attempted_user.password == form.password.data:
                login_user(attempted_user)
                return redirect(url_for('quizhtml'))
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for("home"))

@app.route('/scoreboard')
def scoreboard():
    user_scores = User.query.order_by(User.score.desc()).all()
    return render_template('scoreboard.html', users=user_scores)


if __name__ == "__main__":
    app.run()
    