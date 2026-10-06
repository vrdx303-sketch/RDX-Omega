import socket
import threading
import time

# कॉन्फ़िगरेशन
HOST = "127.0.0.1"
PORT = 8001
BLOCKLIST = set()
REQUEST_COUNTS = {}
RATE_LIMIT_THRESHOLD = 20  # एक तय समय में अधिकतम अनुमति प्राप्त रिक्वेस्ट
TIME_WINDOW = 5

def client_handler(conn, addr):
    ip = addr[0]
    
    # अगर आईपी पहले से ब्लॉक है तो कनेक्शन तुरंत काट दो
    if ip in BLOCKLIST:
        conn.close()
        return

    current_time = time.time()
    if ip not in REQUEST_COUNTS:
        REQUEST_COUNTS[ip] = []

    # पुरानी रिक्वेस्ट को हटाओ
    REQUEST_COUNTS[ip] = [t for t in REQUEST_COUNTS[ip] if current_time - t < TIME_WINDOW]
    REQUEST_COUNTS[ip].append(current_time)

    # रेट लिमिट चेक (अगर फ्लड या हमला करने की कोशिश की)
    if len(REQUEST_COUNTS[ip]) > RATE_LIMIT_THRESHOLD:
        print(f"[!] [RDX SHIELD] Attack detected from {ip}! IP added to permanent blocklist.")
        BLOCKLIST.add(ip)
        conn.close()
        return

    try:
        data = conn.recv(1024)
        if data:
            # हनीपॉट रिस्पॉन्स / सेफ डिफेंसिव रिस्पॉन्स
            response = b"HTTP/1.1 403 Forbidden\r\nServer: RDX-Secure-Fortress\r\nContent-Length: 21\r\n\r\nAccess Denied - RDX"
            conn.sendall(response)
    except Exception:
        pass
    finally:
        conn.close()

def start_secure_shield():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)
    print(f"=== RDX SECURE FORTRESS ACTIVE ON {HOST}:{PORT} ===")
    print("[*] Monitoring traffic, rate-limiting, and honey-pot traps are online...")

    while True:
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=client_handler, args=(conn, addr))
            t.daemon = True
            t.start()
        except Exception as e:
            print(f"[-] Shield error: {e}")
            break

if __name__ == "__main__":
    start_secure_shield()