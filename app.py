from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request,redirect,url_for

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12@localhost/testdb'
app.debug=True
db=SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), unique=True)
    sname = db.Column(db.String(20), unique=True)


    def __init__(self, fname, sname):
        self.fname = fname
        self.sname = sname



    def __repr__(self):
        return '<User %r>' % self.user

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
