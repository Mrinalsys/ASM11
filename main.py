from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secretkey'


def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',  # Replace with your MySQL username
        password='Mrinal123.',  # Replace with your MySQL password
        database='usermanagementdb'  # The name of your database
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', users=users)

# Add a new user
@app.route('/add', methods=('GET', 'POST'))
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        if not first_name or not last_name or not phone or not email or not address:
            flash('All fields are required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO users (first_name, last_name, phone, email, address) VALUES (%s, %s, %s, %s, %s)',
                    (first_name, last_name, phone, email, address)
                )
                conn.commit()
                flash('User added successfully!')
            except mysql.connector.Error as err:
                flash(f'Error: {err}')
            finally:
                cursor.close()
                conn.close()

            return redirect(url_for('index'))

    return render_template('add.html')

# Edit user details
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_user(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        if not first_name or not last_name or not phone or not email or not address:
            flash('All fields are required!')
        else:
            try:
                cursor.execute(
                    'UPDATE users SET first_name = %s, last_name = %s, phone = %s, email = %s, address = %s WHERE id = %s',
                    (first_name, last_name, phone, email, address, id)
                )
                conn.commit()
                flash('User updated successfully!')
            except mysql.connector.Error as err:
                flash(f'Error: {err}')
            finally:
                cursor.close()
                conn.close()

            return redirect(url_for('index'))

    return render_template('edit.html', user=user)

# Delete a user
@app.route('/delete/<int:id>', methods=('POST',))
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = %s', (id,))
        conn.commit()
        flash('User deleted successfully!')
    except mysql.connector.Error as err:
        flash(f'Error: {err}')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

