import socket
import threading

HOST = '127.0.0.1'  # Локальный хост
PORT = 65432        # Порт для прослушивания

def handle_client(conn, addr):
    print(f"Подключено: {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Соединение с {addr} закрыто клиентом.")
                break
            message = data.decode('utf-8').strip()
            print(f"Получено от {addr}: {message}")
            if message.lower() == 'ping':
                response = 'pong'
                conn.sendall(response.encode('utf-8'))
                print(f"Отправлено {addr}: {response}")
            else:
                response = 'error: неизвестная команда'
                conn.sendall(response.encode('utf-8'))
                print(f"Отправлено {addr}: {response}")
    except Exception as e:
        print(f"Ошибка с {addr}: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен и слушает {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()