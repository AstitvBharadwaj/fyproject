from flask import Flask, request, jsonify
import datetime
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize database
def init_db():
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS traffic (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ip TEXT,
                        user_agent TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/track', methods=['POST'])
def track_user():
    data = request.json
    ip = request.remote_addr
    user_agent = data.get('user_agent', 'Unknown')
    timestamp = datetime.datetime.now().isoformat()
    
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO traffic (ip, user_agent, timestamp) VALUES (?, ?, ?)", (ip, user_agent, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User tracked successfully"}), 200

@app.route('/analytics', methods=['GET'])
def get_analytics():
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM traffic")
    data = cursor.fetchall()
    conn.close()
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
