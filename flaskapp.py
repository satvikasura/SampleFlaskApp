from flask import Flask
from flask import render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home_page():
  return render_template('home.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    conn = sqlite3.connect('/var/www/html/flaskapp/user.db')
    cursor = conn.cursor()
    if 'register_btn' in request.form:
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        username = request.form["username"]
        stmnt = "update users set firstName='" + firstName + "', lastName = '" + lastName + "', email = '" + email + "' where username = '" + username + "'"
        cursor.execute(stmnt)
        conn.commit()
        conn.close()
        return render_template('dashboard.html', firstName = firstName, lastName = lastName, email = email)
    elif 'login_btn' in request.form:
        username = request.form["username"]
        password = request.form["password"]
        stmnt = "select firstName, lastName, email from users where username='" + username + "' and password = '" + password + "'"
        cursor.execute(stmnt)
        data = cursor.fetchone()
        conn.commit()
        conn.close()
        if not data:
            return render_template("invalidUser.html")
        else:
            firstName = data[0]
            lastName = data[1]
            email = data[2]
            return render_template('dashboard.html', firstName = firstName, lastName = lastName, email = email)

@app.route('/registrationForm', methods=['POST', 'GET'])
def registrationForm():
    conn = sqlite3.connect('/var/www/html/flaskapp/user.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        if(request.form["username"] != "" and request.form["password"] != ""):
            username = request.form["username"]
            password = request.form["password"]
            stmnt = "select * from users where username='" + username + "'"
            cursor.execute(stmnt)
            data = cursor.fetchone()
            if data:
                conn.commit()
                conn.close()
                return render_template("userExistsError.html")
            else:
                cursor.execute("insert into users(username, password) values (?,?)",(username, password))
                conn.commit()
                conn.close()
                return render_template("registerDetails.html", username = username)
    elif request.method == 'GET':
        return render_template('register.html')

if __name__ == '__main__':
  app.run()

