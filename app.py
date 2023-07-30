from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "sujai"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '20s147@kce.ac.in'  # Replace with your email
app.config['MAIL_PASSWORD'] = '********'  # Replace with your email password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def index():
    try:
        con = mysql.connection.cursor()
        sql = 'select * from student'
        con.execute(sql)
        res = con.fetchall()
        con.close()
        success_message = request.args.get('success_message')
        if success_message:
            return render_template('index.html', data=res, success_message=success_message)
        else:
            return render_template('index.html', data=res)
    except Exception as e:
        return render_template("error.html", error_message=str(e))


@app.route('/addrecord', methods=['GET', 'POST'])
def addrecord():
    try:
        if request.method == 'POST':
            roll = request.form['roll']
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            email = request.form['email']
            dept = request.form['department']
            year = request.form['year']
            ph = request.form['ph']
            con = mysql.connection.cursor()
            sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            con.execute(sql, [roll, name, age, gender, email, dept, year, ph])
            mysql.connection.commit()
            con.close()
            return redirect(url_for('index'))
        return render_template('addrecord.html')
    except Exception as e:
        return render_template("error.html", error_message=str(e))


@app.route("/edit/<string:roll>", methods=['GET', 'POST'])
def edit(roll):
    try:
        con = mysql.connection.cursor()
        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            email = request.form['email']
            dept = request.form['department']
            year = request.form['year']
            ph = request.form['ph']
            upq = 'UPDATE student SET name=%s, age=%s, gender=%s, email_id=%s, dept=%s, year=%s, ph_no=%s WHERE roll_no=%s'
            con.execute(upq, [name, age, gender, email, dept, year, ph, roll])
            mysql.connection.commit()
            con.close()
            return redirect(url_for('index'))
        sql = "SELECT * FROM student WHERE roll_no=%s"
        con.execute(sql, [roll])
        res = con.fetchone()
        con.close()
        return render_template("edit.html", data=res)
    except Exception as e:
        return render_template("error.html", error_message=str(e))


@app.route('/remove/<string:roll>')
def remove(roll):
    try:
        con = mysql.connection.cursor()
        sql = 'DELETE FROM student WHERE roll_no = %s'
        con.execute(sql, [roll])
        mysql.connection.commit()
        con.close()
        success_message = "Record deleted successfully"
        return redirect(url_for('index', success_message=success_message))
    except Exception as e:
        return render_template("error.html", error_message=str(e))


@app.route('/mailedit/<string:mm>', methods=['POST', 'GET'])
def mailedit(mm):
    try:
        if request.method == 'POST':
            rev = request.form['email']
            msg = Message(request.form['subject'], sender='20s147@kce.ac.in', recipients=[rev])
            msg.body = request.form['message']
            mail.send(msg)
            return redirect(url_for('index'))
        return render_template("sendmail.html", data=mm)
    except Exception as e:
        return render_template("error.html", error_message=str(e))


if __name__ == "__main__":
    app.run(debug=True)
