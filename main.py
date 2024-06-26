import socket
import threading

# Определение размера буфера
BUFFER_SIZE = 4096
TARGET_HOST = 'localhost'  # Укажите целевой сервер здесь
TARGET_PORT = 80             # Укажите целевой порт здесь

def handle_client(client_socket):
    try:
        # Получение запроса от клиента
        request = client_socket.recv(BUFFER_SIZE)

        # Создание сокета для соединения с веб-сервером
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((TARGET_HOST))

        # Отправка запроса на веб-сервер
        proxy_socket.send(request)

        while True:
            # Получение данных от веб-сервера
            data = proxy_socket.recv(BUFFER_SIZE)

            if len(data) > 0:
                # Отправка данных клиенту
                client_socket.send(data)
            else:
                break

        proxy_socket.close()
        client_socket.close()

    except Exception as e:
        print(f"Ошибка обработки клиента: {e}")
        client_socket.close()

def start_proxy_server():
    # Создание сокета для прокси-сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Связывание сокета с локальным адресом и портом
    server_socket.bind(('0.0.0.0', 8888))
    server_socket.listen(5)

    print('Прокси-сервер запущен на порту 8888...')

    while True:
        try:
            # Принятие входящего соединения
            client_socket, addr = server_socket.accept()
            print(f"Получено соединение от {addr}")

            # Создание нового потока для обработки клиента
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
        except KeyboardInterrupt:
            print("Завершение работы прокси-сервера")
            server_socket.close()
            break
        except Exception as e:
            print(f"Ошибка при принятии соединения: {e}")

if __name__ == '__main__':
    start_proxy_server()
