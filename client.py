import socket
import time

HOST = '127.0.0.1'  # Адрес сервера
PORT = 65432        # Порт сервера

def client_behaviour():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Клиент: Подключение к серверу...")
            s.connect((HOST, PORT))
            print("Клиент: Подключен.")

            for i in range(5):  # Отправим 5 ping
                message = 'ping'
                print(f"Клиент: Отправка -> {message}")
                s.sendall(message.encode('utf-8'))

                data = s.recv(1024)
                if not data:
                    print("Клиент: Соединение закрыто сервером.")
                    break
                response = data.decode('utf-8').strip()
                print(f"Клиент: Получено -> {response}")

                if response != 'pong':
                    print("Клиент: Ошибка в ответе от сервера.")
                    break
                time.sleep(1)  # Ждём 1 секунду перед следующим ping

    except ConnectionRefusedError:
        print("Клиент: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Клиент: Произошла ошибка: {e}")

if __name__ == "__main__":
    client_behaviour()

