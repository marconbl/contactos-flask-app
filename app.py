from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Inicializacion
app = Flask(__name__)

# Conexion a Mysql 
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'marcosnbl'
app.config['MYSQL_PASSWORD'] = 'mnbl38778'
app.config['MYSQL_DB'] = 'marcosnbl'
mysql = MySQL(app)

# ajustes
app.secret_key = "mysecretkey"

# rutas
@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contactos')
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', contactos = data)

@app.route('/agregar_contactos', methods=['POST'])
def agregar_contactos():
    if request.method == 'POST':
        nombrecompleto = request.form['nombrecompleto']
        telefono = request.form['telefono']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO contactos (nombrecompleto, telefono, email) VALUES (%s,%s,%s)", (nombrecompleto, telefono, email))
        mysql.connection.commit()
        flash('Contacto Agregado Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/editar/<id>', methods = ['POST', 'GET'])
def get_contactos(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contactos WHERE id = %s', (id))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('editar-contacto.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def actualizar_contactos(id):
    if request.method == 'POST':
        nombrecompleto = request.form['nombrecompleto']
        telefono = request.form['telefono']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE contactos
            SET nombrecompleto = %s,
                email = %s,
                telefono = %s
            WHERE id = %s
        """, (nombrecompleto, email, telefono, id))
        flash('Contacto Actualizado Correctamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/eliminar/<string:id>', methods = ['POST','GET'])
def eliminar_contactos(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Eliminado Sastisfoctariamnte')
    return redirect(url_for('Index'))

# Inicia la Aplicacion
if __name__ == "__main__":
    app.run(port=3000, debug=True)