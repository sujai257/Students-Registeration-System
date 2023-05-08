from flask import Flask,render_template,redirect,url_for
from flask_mysqldb import MySQL
from flask.templating import render_template_string
from flask.globals import request
from pip._internal import req
from test.test_contains import seq
from flask_mail import Mail,Message
app =Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="sujai"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

mail = Mail(app) 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mailid@gmail.com'
app.config['MAIL_PASSWORD'] = '******'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    con = mysql.connection.cursor()
    sql ='select * from student'
    con.execute(sql)
    res=con.fetchall()
    success_message = request.args.get('success_message')
    if success_message:
        return render_template('index.html', data=res, success_message=success_message)
    else:
        return render_template('index.html', data=res)   

@app.route('/addrecord',methods=['GET','POST'])
def addrecord():
    if(request.method=='POST'):
        roll=request.form['roll']
        name=request.form['name']
        age=request.form['age']
        gender=request.form['gender']
        email=request.form['email']
        dept=request.form['department']
        year=request.form['year']
        ph=request.form['ph']
        con=mysql.connection.cursor()
        try:      
            sql="insert into student values(%s,%s,%s,%s,%s,%s,%s,%s);"
            con.execute(sql,[roll,name,age,gender,email,dept,year,ph])
            mysql.connection.commit()
        except:
            return render_template("error.html")
        con.close()
        return redirect(url_for('index'))
    return render_template('addrecord.html')

@app.route("/edit/<string:roll>",methods=['GET','POST'])
def edit(roll):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        gender=request.form['gender']
        email=request.form['email']
        dept=request.form['department']
        year=request.form['year']
        ph=request.form['ph']
        upq='update student  set name=%s,age=%s,gender=%s,email_id=%s,dept=%s,year=%s,ph_no=%s where roll_no=%s'
        con.execute(upq,[name,age,gender,email,dept,year,ph,roll])
        mysql.connection.commit()
        con.close()
        return redirect(url_for('index'))
    con=mysql.connection.cursor()
    sql="select * from student where roll_no=%s"
    con.execute(sql,[roll])
    res=con.fetchone()    
    return render_template("edit.html",data =res)

@app.route('/remove/<string:roll>')
def remove(roll):
    con = mysql.connection.cursor()
    sql = 'DELETE FROM student WHERE roll_no = %s'
    con.execute(sql, [roll])
    mysql.connection.commit()
    con.close()
    success_message = "Record deleted successfully"
    return redirect(url_for('index', success_message=success_message))

@app.route('/mailedit/<string:mm>',methods=['POST','GET'])
def mailedit(mm):
    if request.method=='POST':
        try:       
            rev= request.form ['email'] 
            msg = Message(request.form['subject'],sender ='mailid@gmail.com',recipients = [rev])
            msg.body = request.form['message']
            mail.send(msg)
        except:
            return render_template('error.html')
        else:
            return redirect(url_for('index'))       
    return render_template("sendmail.html",data =mm)   
if __name__ == ("__main__"):
    app.run(debug=True) 


     