import os
import random
import mysql.connector
from flask import Flask, request, jsonify

# Configura Flask
app = Flask(__name__)

# Configurazione del database
db_config = {
    'host': os.getenv('MYSQL_HOST', 'db'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'root'),
    'database': os.getenv('MYSQL_DATABASE', 'password_db')
}

def generate_password(length=12, use_special_chars=True, use_numbers=True):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_special_chars:
        characters += "!@#$%^&*()"
    if use_numbers:
        characters += "0123456789"
    password = "".join(random.choice(characters) for _ in range(length))
    return password

def save_password_to_db(password, label):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS passwords (id INT AUTO_INCREMENT PRIMARY KEY, label VARCHAR(255), password VARCHAR(255))")
        cursor.execute("INSERT INTO passwords (label, password) VALUES (%s, %s)", (label, password))
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Errore: {err}")

@app.route('/generate_password', methods=['POST'])
def generate_password_endpoint():
    # Prende i parametri dalla richiesta JSON
    data = request.get_json()
    length = data.get("length", 12)
    use_special_chars = data.get("use_special_chars", True)
    use_numbers = data.get("use_numbers", True)
    label = data.get("label", "Generico")
    
    # Genera la password
    password = generate_password(length, use_special_chars, use_numbers)
    
    # Salva la password nel database con l'etichetta
    save_password_to_db(password, label)
    
    return jsonify({"label": label, "password": password})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
