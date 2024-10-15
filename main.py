from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np
import database as db
from filo_nlp import classifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from collections import Counter
import datetime
from models.knn_model import KNNManual

data = pd.read_csv('dataset.csv')
X = data.iloc[:, :10] 
y = data.iloc[:, 10]  

le = LabelEncoder()
y = le.fit_transform(y)

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.5, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

k = 5
knn_manual = KNNManual(k=k)
knn_manual.fit(X_train.values, y_train)

app = Flask(__name__)
app.secret_key = 'my_secret'
register_list = []
values = {}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('inicio'))
    else:
        return redirect(url_for('welcome'))

@app.route("/bienvenido")
def welcome():
    if 'username' in session:
        return render_template('forum.html', username=session['username'])
    else:
        return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global values
        values = {key: val for key, val in request.form.items()}
        db.database.reconnect()
        
        # Checa si se está logueando a registrando un usuario
        if len(values) > 2:
            cursor = db.database.cursor()
            sql = 'SELECT * FROM users WHERE user1 = (%s) AND userPassword = (%s)'
            data = (values['username'], values['password'])
            cursor.execute(sql, data)
            row = cursor.fetchone()
            if row:
                flash('¡Usuario Ya Registrado!')
                return redirect(url_for('login'))
            else:
                return redirect(url_for('register1'))
        else:
            cursor = db.database.cursor()
            sql = 'SELECT idUsers, user1, userPassword FROM users WHERE user1 = (%s) AND userPassword = (%s)'
            data = (values['username'], values['password'])
            cursor.execute(sql, data)
            row = cursor.fetchone()
            if row:
                session['username'] = values['username']
                session['idUser'] = row[0]
                return redirect(url_for('forum'))
            else:
                flash('¡Datos Incorrectos!')
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register1', methods=['GET', 'POST'])
def register1():
    register_list.clear()
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    return render_template('register1.html')

@app.route('/register2', methods=['GET', 'POST'])
def register2():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    return render_template('register2.html')

@app.route('/register3', methods=['GET', 'POST'])
def register3():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    return render_template('register3.html')

@app.route('/register4', methods=['GET', 'POST'])
def register4():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    return render_template('register4.html')

@app.route('/register5', methods=['GET', 'POST'])
def register5():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    return render_template('register5.html')

@app.route('/register6', methods=['GET', 'POST'])
def register6():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    return render_template('register6.html')

@app.route('/register7', methods=['GET', 'POST'])
def register7():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    else:
        return render_template('register7.html')

@app.route('/register8', methods=['GET', 'POST'])
def register8():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    else:
        return render_template('register8.html')

@app.route('/register9', methods=['GET', 'POST'])
def register9():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        print(data)
    else:
        return render_template('register9.html')

@app.route('/register10', methods=['GET', 'POST'])
def register10():
    data = request.form.get('data')
    if data:
        register_list.append(data)
        for i in register_list:
            print(i)
    # Asegúrate de devolver una respuesta independientemente de si se añadió `data` o no
    return render_template('register10.html')

@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    db.database.reconnect()
    cursor = db.database.cursor()
    sql = "INSERT INTO users (userName, userLastName, user1, userPassword) VALUES (%s, %s, %s, %s)"
    data = (values['name'], values['second_name'], values['username'], values['password'])
    cursor.execute(sql, data)
    db.database.commit()

    # Recuperar el 'id_usuario' del usuario recién insertado usando su 'usuario'
    sql_get_id = "SELECT idUsers FROM users WHERE user1 = %s"
    cursor.execute(sql_get_id, (values['username'],))
    id_usuario = cursor.fetchone()[0]
    
    session['idUser'] = id_usuario

    # Insertar los datos en la tabla 'indices' usando el 'id_usuario'
    sql2 = "INSERT INTO indexes (idUsers, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data2 = (id_usuario, register_list[0], register_list[1], register_list[2], register_list[3], register_list[4], register_list[5], register_list[6], register_list[7], register_list[8], register_list[9])
    cursor.execute(sql2, data2)

    # Confirmar las operaciones en la base de datos
    db.database.commit()

    # Iniciar sesión con el nombre de usuario registrado
    session['username'] = values['username']

    return redirect(url_for('clasificar'))

@app.route('/clasificar', methods=['GET', 'POST'])
def clasificar():
    input_values = []
    for value in register_list[:10]:  # Limitar a los primeros 10 valores
        try:
            input_values.append(float(value))
        except ValueError:
            flash("Datos inválidos en register_list, asegúrate de que todos sean numéricos.")
            return redirect(url_for('dashboard'))

    # Si tienes más datos de entrada que necesitas
    for i in range(1, 11):
        valor = request.form.get(f'feature{i}')
        if valor:
            try:
                input_values.append(float(valor))
            except ValueError:
                flash(f"Valor inválido para feature{i}: {valor}")
                return redirect(url_for('dashboard'))

    # Limitar a 10 valores en caso de que se hayan agregado más
    input_values = input_values[:10]  

    nuevo_input = np.array([input_values])
    
    # Asegúrate de que el número de valores coincida con las columnas de X_train
    if len(input_values) != 10:
        flash("El número de entradas no es válido. Asegúrate de ingresar exactamente 10 valores.")
        return redirect(url_for('dashboard'))


    nuevo_input = np.array([input_values])
    prediccion = knn_manual.predict(nuevo_input)
    prediccion_original = le.inverse_transform(prediccion)[0]
    
    cursor = db.database.cursor()
    id_usuario = session.get('idUser')  # Obtener el 'id_usuario' de la sesión
    
    sql2 = "UPDATE indexes SET class = %s WHERE idUsers = %s"
    data2 = (prediccion_original, id_usuario)
    cursor.execute(sql2, data2)

    db.database.commit()
    if prediccion_original == 'Platonismo':
        return render_template('filo_templates/platonismo.html')
    elif prediccion_original == 'Aristotelismo':
        return render_template('filo_templates/aristotelismo.html')
    elif prediccion_original == 'Idealismo':
        return render_template('filo_templates/idealismo.html')
    elif prediccion_original == 'Estoicismo':
        return render_template('filo_templates/estoicismo.html')
    elif prediccion_original == 'Realismo':
        return render_template('filo_templates/realismo.html')
    elif prediccion_original == 'Racionalismo':
        return render_template('filo_templates/racionalismo.html')
    elif prediccion_original == 'Empirismo':
        return render_template('filo_templates/empirismo.html')
    elif prediccion_original == 'Humanismo':
        return render_template('filo_templates/humanismo.html')
    elif prediccion_original == 'Existencialismo':
        return render_template('filo_templates/existencialismo.html')
    elif prediccion_original == 'Hedonismo':
        return render_template('filo_templates/hedonismo.html')
    elif prediccion_original == 'Nihilismo':
        return render_template('filo_templates/nihilismo.html')
    elif prediccion_original == 'Cinismo':
        return render_template('filo_templates/cinismo.html')
    else:
        return render_template('resultado.html', resultado=prediccion_original)


@app.route('/forum', methods=['GET', 'POST'])
def forum():
    cursor = db.database.cursor()
    sql = 'SELECT users.user1,title, body, filo_school, date, nlp_result, posts.idPosts from posts JOIN users ON posts.idUsersP = users.idUsers'
    cursor.execute(sql)
    posts = cursor.fetchall()
    return render_template('forum.html', posts=posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user = session['idUser']

        cursor = db.database.cursor()
        cursor.execute('SELECT class from indexes where idUsers = (%s)', (user,))
        school = cursor.fetchone()[0]
        result = classifier(body)
        if result == 'No se pudo clasificar':
            result = school
        print(f"Escuela: {result}")
        
        sql = 'INSERT INTO posts (idUsersP, title, body, filo_school, date, nlp_result) VALUES (%s, %s, %s, %s, now(), %s)'
        values = (user, title, body, school, result)
        cursor.execute(sql, values)
        db.database.commit()

        return redirect(url_for('forum'))
    return render_template('post.html')

@app.route('/post/<post_id>')
def post_details(post_id):
    cursor = db.database.cursor()

    # Obtener la publicación específica
    cursor.execute('SELECT users.user1, title, body, date, nlp_result, idPosts FROM posts JOIN users ON posts.idUsersP = users.idUsers WHERE posts.idPosts = %s', (post_id,))
    post = cursor.fetchone()

    # Obtener todos los comentarios de la publicación
    cursor.execute('SELECT comments.comment, comments.date, users.user1 FROM comments JOIN users ON comments.idUsersC = users.idUsers WHERE comments.idPostsC = %s ORDER BY comments.date', (post_id,))
    comments = cursor.fetchall()

    # Renderizar la plantilla con la publicación y los comentarios
    return render_template('post_details.html', post=post, comments=comments)

@app.route('/add_comment/<post_id>', methods=['POST'])
def add_comment(post_id):
    # Verificar si el usuario ha iniciado sesión
    if 'idUser' not in session:
        flash('Debes iniciar sesión para comentar.')
        return redirect(url_for('login'))

    comentario = request.form.get('comentario')
    
    if comentario and comentario.strip():
        cursor = db.database.cursor()
        # Insertar el nuevo comentario en la base de datos
        sql = "INSERT INTO comments (idPostsC, idUsersC, comment,date) VALUES (%s, %s, %s,now())"
        cursor.execute(sql, (post_id, session['idUser'], comentario))
        db.database.commit()
        flash('Comentario añadido correctamente.')
    else:
        flash('El comentario no puede estar vacío.')
    
    # Redirigir de vuelta a la página de detalles del post
    return redirect(url_for('post_details', post_id=post_id))

@app.route('/inicio', methods=['GET'])
def inicio():
    # Consulta para obtener los datos del usuario autenticado
    user_id = session['idUser']  # Simulación del ID de usuario (debes cambiarlo según corresponda)
    cursor = db.database.cursor()
    # Consulta para obtener los detalles del usuario y su clase filosófica
    cursor.execute('SELECT u.userName, u.userLastName,u.user1, i.class FROM users u, indexes i WHERE u.idUsers = i.idUsers AND u.idUsers = (%s)', (user_id,))
    user_info = cursor.fetchone()


    # Estructura de datos para pasar a la plantilla HTML
    user_data = {
        'nombres': user_info[0],
        'apellidos': user_info[1],
        'usuario': user_info[2],
        'clase': user_info[3],
        'fecha_registro': '2023-05-12'  # Cambia esta fecha por la que esté en tu base de datos
    }

    # Consulta de las últimas publicaciones del usuario
    sql_posts = '''
        SELECT title, body, date, nlp_result 
        FROM posts 
        WHERE idUsersP = (%s)
        ORDER BY date DESC 
        LIMIT 5
    '''
    cursor.execute(sql_posts, (user_id,))
    user_posts = cursor.fetchall()

    return render_template('inicio.html', user_data=user_data, user_posts=user_posts)
@app.route('/escuelas_filo')
def escuelas_filo():
    if 'username' in session:
        return render_template('escuelas_filo.html')

@app.route('/aristotelismo')
def aristotelismo():
    if 'username' in session:
        return render_template('/filo_templates/aristotelismo.html')
    
@app.route('/cinismo')
def cinismo():
    if 'username' in session:
        return render_template('/filo_templates/cinismo.html')
    
@app.route('/empirismo')
def empirismo():
    if 'username' in session:
        return render_template('/filo_templates/empirismo.html')
    
@app.route('/estoicismo')
def estoicismo():
    if 'username' in session:
        return render_template('/filo_templates/estoicismo.html')
    
@app.route('/existencialismo')
def existencialismo():
    if 'username' in session:
        return render_template('/filo_templates/existencialismo.html')
    
@app.route('/hedonismo')
def hedonismo():
    if 'username' in session:
        return render_template('/filo_templates/hedonismo.html')
    
@app.route('/humanismo')
def humanismo():
    if 'username' in session:
        return render_template('/filo_templates/humanismo.html')
    
@app.route('/idealismo')
def idealismo():
    if 'username' in session:
        return render_template('/filo_templates/idealismo.html')
    
@app.route('/nihilismo')
def nihilismo():
    if 'username' in session:
        return render_template('/filo_templates/nihilismo.html')
    
@app.route('/platonismo')
def platonismo():
    if 'username' in session:
        return render_template('/filo_templates/platonismo.html')
    
@app.route('/racionalismo')
def racionalismo():
    if 'username' in session:
        return render_template('/filo_templates/racionalismo.html')
    
@app.route('/realismo')
def realismo():
    if 'username' in session:
        return render_template("/filo_templates/realismo.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('idUser', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
