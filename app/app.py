#Esta es la clase que se encarga de arrancar la aplicacion, archivo inicial del servidor

#importo el framework flask 
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

#conexion mysql
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flask_to_do_list'
mysql= MySQL(app)

#inicializacion de una sesion 
app.secret_key='mysecretkey'

# esto es un decorador que me ayuda a que cuando el cliente solicita la ruta principal va a responder algo
#defino una funcion para poder manejar la ruta ejemplo index y retornar algun valor
@app.route('/')
def Index ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tareas where tarea_realizada=false ')
    data=cur.fetchall()
    return render_template('index.html', tareas= data)
#Ruta principal de la aplicacion
@app.route('/add_tarea', methods= ['POST'])
def add_tarea():
    if request.method == 'POST':
        nombre= request.form['nombre_tarea']
        desc= request.form['descripcion']
        print(nombre)
        print(desc)
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO tareas (nombre_tarea, descripcion) values(%s, %s)', (nombre, desc))
        mysql.connection.commit()
        flash('Tarea agregada satisfactoriamente')
        #para redireccionar a una ruta, importo las clases redirect y ur_for y agrego lo soguiente
        #lo que va dentro de url_for es el nombre del metodo que ejecuta el index
        return redirect(url_for('Index'))

#ruta para eliminar un dato de la tabla
@app.route('/eliminar/<string:id>')
def eliminar_tarea(id):
    cur= mysql.connection.cursor()
    cur.execute('DELETE FROM tareas WHERE id ={0}'.format(id))
    mysql.connection.commit()
    flash('Tarea removida')
    return redirect(url_for('Index'))

#ruta para editar una tarea
@app.route('/editar/<id>')
def editar_tarea(id):
    cur= mysql.connection.cursor()
    cur.execute('Select * from tareas where id= %s', [id])
    tarea=cur.fetchall()
    return render_template('editar_tarea.html', tareas= tarea[0])

# ruta para guardar los datos de la tarea a editar
@app.route('/guardar_edit/<id>', methods = ['POST'])
def guardar_cambios(id):
    if request.method == 'POST':
        nombre= request.form['nombre_tarea']
        desc= request.form['descripcion']
        cur= mysql.connection.cursor()
        cur.execute("""
        UPDATE  tareas
            SET nombre_tarea=%s,
                descripcion= %s
        WHERE id=%s
        """, (nombre, desc,id))
        mysql.connection.commit()
        flash('Tarea actualizada')
        return redirect(url_for('Index'))

#ruta para marcar una tarea como terminada y que desaparezca de la tabla
@app.route('/terminar/<string:id>')
def terminar_tarea(id):
    print(id)
    cur= mysql.connection.cursor()
    cur.execute("""
        UPDATE tareas
        SET tarea_realizada= true
        WHERE id=%s
    """, [id])
    mysql.connection.commit()
    flash('Tarea terminada')
    return redirect(url_for('Index'))

#ruta para ver las tareas que estan terminadas
@app.route('/ver_tareas_terminadas')
def ver_tareas():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM tareas WHERE tarea_realizada= true')
    data= cur.fetchall()
    return render_template('tareas_terminadas.html', tareas= data)

#aca verifico que se este ejecutando la clase principal
if __name__ == '__main__':
    app.run(port=3000, debug= True)
#para empezar a ejecutar el servidor y le asigno el puerto 3000
# el debu ayuda a que cuando haga un cambio se reinicie el servidor automaticamente