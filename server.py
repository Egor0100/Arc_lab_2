import socket
import threading

HOST = '127.0.0.1'  # Локальный хост для прослушивания
PORT = 65432  # Порт для прослушивания входящих соединений


def handle_client(conn, addr):
    """
    Обработчик подключений от клиентов.

    Принимает сообщения от клиента, отвечает "pong" на "ping" и
    "error: неизвестная команда" на другие сообщения.

    :param conn: Сокетное соединение с клиентом.
    :param addr: Адрес клиента.
    """
    print(f"Подключено: {addr}")
    try:
        while True:
            # Принимаем данные от клиента (до 1024 байт)
            data = conn.recv(1024)
            if not data:
                # Если данных нет, клиент закрыл соединение
                print(f"Соединение с {addr} закрыто клиентом.")
                break
            # Декодируем полученные данные
            message = data.decode('utf-8').strip()
            print(f"Получено от {addr}: {message}")

            # Обработка сообщения
            if message.lower() == 'ping':
                response = 'pong'
            else:
                response = 'error: неизвестная команда'

            # Отправляем ответ клиенту
            conn.sendall(response.encode('utf-8'))
            print(f"Отправлено {addr}: {response}")
    except Exception as e:
        # Обработка исключений во время общения с клиентом
        print(f"Ошибка с {addr}: {e}")
    finally:
        # Закрываем соединение
        conn.close()


def start_server():
    """
    Функция запуска сервера.

    Создаёт TCP-сокет, привязывает его к указанному хосту и порту,
    начинает прослушивание входящих соединений и обрабатывает их в отдельных потоках.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Привязываем сокет к адресу и порту
        s.bind((HOST, PORT))
        # Начинаем прослушивание (максимум 5 ожидающих соединений)
        s.listen()
        print(f"Сервер запущен и слушает {HOST}:{PORT}")

        while True:
            # Принимаем новое соединение
            conn, addr = s.accept()
            # Создаём новый поток для обработки клиента
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == "__main__":
    start_server()
