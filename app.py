from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Radarada1218'
app.config['MYSQL_DB']='projectpython'

mysql = MySQL(app)

app.secret_key = 'lock'
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    students = cur.fetchall()
    print(students)
    return render_template('Index.html', student = students)

@app.route('/Add', methods=['POST'])
def Add():
    if request.method == 'POST':
        enrollment = request.form['Enrollment']
        name = request.form['Name']
        lastname = request.form['Lastname']
        age = request.form['Age']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Students VALUE(%s, %s, %s, %s)', (enrollment, name, lastname, age))
        mysql.connection.commit()
        flash("Estudiante agregado con exito")
        return redirect(url_for('Index'))

@app.route('/Update/<Enrollment>')
def Update(Enrollment):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students WHERE Enrollment = "{0}"'.format(Enrollment))
    Student = cur.fetchall()
    return render_template('Update.html', students = Student[0])


@app.route('/Update/<id>', methods=['POST'])
def UpdatePOST(id):
    if request.method == 'POST':
        enrollment = request.form['Enrollment']
        name = request.form['Name']
        lastname = request.form['Lastname']
        age = request.form['Age']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE Students SET Enrollment =%s, Name = %s, Lastname=%s, Age=%s WHERE Enrollment=%s', (enrollment, name, lastname, age, enrollment))
        mysql.connection.commit()
        flash("Estudiante actualizado con exito")
        return redirect(url_for('Index'))

@app.route('/Delete/<string:Enrollment>')
def Delete(Enrollment):
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Students WHERE Enrollment = "{0}"'.format(Enrollment))
        mysql.connection.commit()
        flash("Estudiante Eliminado con exito {0}".format(Enrollment))
        return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
