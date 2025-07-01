# socket_hub.py

from flask_socketio import SocketIO
import socket
import json


class SocketHub:
    def __init__(self, app, port: int = 678):
        self.socketio = SocketIO(app)  # Khởi tạo SocketIO với Flask app
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', port))

    def emit(self, event, data):
        self.socketio.emit(event, data)  # Phát sự kiện đến tất cả client

            
    def receive_udp(self):
        '''receive udp broadcast and emit to client'''
        while True:
            raw_data, addr = self.socket.recvfrom(1024)
            data = json.loads(raw_data.decode('utf-8'))
            self.emit('udp_message', {'from': addr, 'message': data['message'], 'type': data['message_type']})
            

    # threading.Thread(target=receive_udp_broadcast, daemon=True).start()