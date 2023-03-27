from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapp'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        ID = request.form['ID']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        DOB = request.form['DOB']
        amount = request.form['amount']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (ID, firstname, lastname, DOB, amount)  VALUES (%s, %s, %s, %s, %s)", (ID, firstname, lastname, DOB, amount))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        ID = request.form['ID']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        DOB = request.form['DOB']
        amount = request.form['amount']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET firstname=%s, lastname=%s, DOB=%s, amount=%s
               WHERE ID=%s
            """, (firstname, lastname, DOB, amount, ID))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))



@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE ID=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)