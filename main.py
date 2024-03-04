from flask import Flask, render_template, request, redirect, url_for
import socket
import json
from datetime import datetime
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        
        # Sending data to socket server
        send_to_socket(username, message)
        
        return redirect(url_for('index'))
    return render_template('message.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

def send_to_socket(username, message):
    data = {
        "username": username,
        "message": message
    }
    json_data = json.dumps(data)
    # Sending data to socket server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(json_data.encode(), ('localhost', 5000))
    client_socket.close()

def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))

    while True:
        data, addr = server_socket.recvfrom(1024)
        message_data = json.loads(data.decode())

        # Saving data to JSON file
        with open('storage/data.json', 'a') as file:
            timestamp = datetime.now().isoformat()
            json.dump({timestamp: message_data}, file)
            file.write('\n')

    server_socket.close()

if __name__ == '__main__':
    # Running socket server in a separate thread
    socket_thread = threading.Thread(target=socket_server)
    socket_thread.start()

    # Running Flask app
    app.run(port=3000)
