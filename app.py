from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask_security import RoleMixin,Security,SQLAlchemyUserDatastore,UserMixin


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12@localhost/testdb'
app.debug=True
db=SQLAlchemy(app)

# Define models from python hosted

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



@app.route('/')
def index():
    return render_template('add_user.html')

@app.route('/profile/<email>')

def profile(email):
    user = User.query.filter_by(email=email).first()
    return render_template('profile.html', user=user)

@app.route('/post_user', methods=['POST'])
def post_user():
    user=User(request.form['fname'],request.form['sname'])
    db.session.add(user)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run()
