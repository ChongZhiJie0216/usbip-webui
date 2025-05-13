import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from usbip_utils import list_devices, bind_device, unbind_device
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

last_state = []

def poll_devices():
    global last_state
    while True:
        try:
            current = list_devices()
            if current != last_state:
                last_state = current
                socketio.emit('update', current)
        except Exception as e:
            print(f"[poll_devices error] {e}")
        time.sleep(3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/devices', methods=['GET'])
def devices():
    return jsonify(list_devices())

@app.route('/bind', methods=['POST'])
def bind():
    busid = request.json.get('busid')
    if bind_device(busid):
        socketio.emit('update', list_devices())
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'}), 500

@app.route('/unbind', methods=['POST'])
def unbind():
    busid = request.json.get('busid')
    if unbind_device(busid):
        socketio.emit('update', list_devices())
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'}), 500

if __name__ == '__main__':
    threading.Thread(target=poll_devices, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
