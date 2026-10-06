import os

def build_zetta_recovery_system():
    print("[*] Jhatka System Auto-Builder Started...")

    # तेरे मौजूदा फोल्डर्स के पाथ
    db_folder = "database"
    frontend_folder = "public_frontend"

    # 1. डेटाबेस रिकवरी मैनेजर बनाना
    db_file_path = os.path.join(db_folder, "recovery_manager.py")
    db_code = """import sqlite3
import os

DB_PATH = os.path.join('database', 'users_data.db')

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            user_id TEXT,
            message TEXT,
            reply TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("[+] Database Ready at", DB_PATH)

def save_chat(user_id, message, reply):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats VALUES (?, ?, ?)", (user_id, message, reply))
    conn.commit()
    conn.close()

def recover_data(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT message, reply FROM chats WHERE user_id=?", (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history
"""
    with open(db_file_path, "w", encoding="utf-8") as f:
        f.write(db_code)
    print(f"[+] Created {db_file_path}")

    # 2. वाइट पेज (HTML) बनाना
    html_file_path = os.path.join(frontend_folder, "index.html")
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Zetta Engine - White Page</title>
    <style>
        body { font-family: Arial; padding: 40px; background: #fff; }
        .box { border: 1px solid #000; padding: 20px; width: 60%; margin: auto; }
        #chat-history { height: 300px; overflow-y: scroll; border: 1px solid #ddd; margin-bottom: 20px; padding: 10px; }
        button { background: black; color: white; padding: 10px; cursor: pointer; border: none; }
        .recovery-btn { background: red; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Jhatka Engine: White Page</h2>
        <button class="recovery-btn" onclick="recoverData()">🔄 Recover My Data</button>
        <div id="chat-history"></div>
        <input type="text" id="userInput" placeholder="Type here..." style="width:70%; padding:10px;">
        <button onclick="sendData()">Send</button>
    </div>

    <script>
        function sendData() {
            let text = document.getElementById('userInput').value;
            document.getElementById('chat-history').innerHTML += '<p><b>You:</b> ' + text + '</p>';
            // यहाँ बाद में तेरा FastAPI बैकएंड जुड़ेगा
        }
        function recoverData() {
            alert("Connecting to Jhatka Engine... fetching local SSD data!");
        }
    </script>
</body>
</html>
"""
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"[+] Created {html_file_path}")

    print("[*] Jhatka Builder Success! Files are ready to be linked with main.py")

if __name__ == "__main__":
    build_zetta_recovery_system()