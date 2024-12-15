import socket
import time

HOST = '127.0.0.1'  # Адрес сервера (локальный хост)
PORT = 65432  # Порт сервера для подключения


def client_behaviour():
    """
    Функция поведения клиента.

    Устанавливает соединение с сервером и отправляет 5 сообщений "ping",
    ожидая ответа "pong" от сервера. Между отправками ожидает 1 секунду.
    """
    try:
        # Создаём TCP-сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Клиент: Подключение к серверу...")
            # Устанавливаем соединение с сервером
            s.connect((HOST, PORT))
            print("Клиент: Подключен.")

            # Отправляем 5 сообщений "ping"
            for i in range(5):
                message = 'ping'
                print(f"Клиент: Отправка -> {message}")
                # Отправляем сообщение, кодированное в UTF-8
                s.sendall(message.encode('utf-8'))

                # Ожидаем ответ от сервера (до 1024 байт)
                data = s.recv(1024)
                if not data:
                    print("Клиент: Соединение закрыто сервером.")
                    break
                # Декодируем полученные данные
                response = data.decode('utf-8').strip()
                print(f"Клиент: Получено -> {response}")

                # Проверяем корректность ответа
                if response != 'pong':
                    print("Клиент: Ошибка в ответе от сервера.")
                    break
                # Ждём 1 секунду перед следующей отправкой
                time.sleep(1)

    except ConnectionRefusedError:
        # Обрабатываем ошибку отсутствия подключения к серверу
        print("Клиент: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        # Обрабатываем все остальные возможные ошибки
        print(f"Клиент: Произошла ошибка: {e}")


if __name__ == "__main__":
    client_behaviour()

