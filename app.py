from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)
app.secret_key = '20040214'

DB_CONFIG = {
    'dbname': 'site',
    'user': 'kris',
    'password': '12345',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    user_contact = request.json.get('contact')
    if not user_contact:
        return jsonify({'status': 'error', 'message': 'Пожалуйста, введите контактные данные.'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Ошибка подключения к базе данных.'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO \"user\" (user_id) VALUES (%s)", (user_contact,))
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        return jsonify({'status': 'error', 'message': f'Ошибка выполнения запроса: {e}'}), 500
    finally:
        conn.close()

    return jsonify({'status': 'success', 'message': 'Контактные данные успешно сохранены!'})

if __name__ == '__main__':
    app.run(debug=True)
