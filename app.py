from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request,redirect,url_for

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


@app.route('/')
def index():
    return render_template('adduser.html')

@app.route('/post_user', methods=['POST'])
def post_user():
    user=User(request.form['fname'],request.form['sname'])
    db.session.add(user)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run()
