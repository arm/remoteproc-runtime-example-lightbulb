import os
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

current_state = "off"
state_lock = threading.Lock()

DEVICE_PATH = "/dev/ttyRPMSG0"
HOST = "0.0.0.0"
PORT = 3000



def activate_rpmsgtty():
    """Best-effort activation by writing a char to the device."""
    import time

    # Wait for device to appear (up to 30 seconds)
    for _ in range(30):
        if os.path.exists(DEVICE_PATH):
            break
        print(f"HACK: {DEVICE_PATH} not present yet; waiting...")
        time.sleep(1)

    try:
        if not os.path.exists(DEVICE_PATH):
            print(f"HACK: {DEVICE_PATH} not present after 30s; skipping activation")
            return

        with open(DEVICE_PATH, "w") as device:
            device.write("0")
            device.flush()

        print(f"HACK: Wrote activation byte to {DEVICE_PATH}")
    except Exception as err:
        print(f"HACK: Failed to activate {DEVICE_PATH}: {err}")


def monitor_rpmsgtty():
    """
    Background thread monitoring {DEVICE_PATH} for changes.
    Reads newline deliminated messages from tty stream
    """
    global current_state

    print("Starting rpmsgtty monitor thread")

    while True:
        try:
            if not os.path.exists(DEVICE_PATH):
                print(f"Waiting for {DEVICE_PATH} to appear...")
                socketio.sleep(2)
                continue

            print(f"Opening {DEVICE_PATH}...")
            with open(DEVICE_PATH, "r") as device:
                print(
                    f"Successfully opened {DEVICE_PATH}, monitoring for state changes..."
                )

                while True:
                    line = device.readline()

                    if not line:
                        # Device disconnected (EOF)
                        print(f"Device {DEVICE_PATH} disconnected")
                        break

                    state = line.strip().lower()

                    if state in ["on", "off"]:
                        with state_lock:
                            if state != current_state:
                                current_state = state
                                print(f"State changed to: {state}")

                                # Broadcast state change to all connected clients
                                socketio.emit(
                                    "state_update", {"state": state}, namespace="/"
                                )
                    else:
                        print(f"Received unexpected message: {repr(line)}")

        except Exception as e:
            print(f"Error reading from {DEVICE_PATH}: {e}")
            socketio.sleep(2)


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html", initial_state=current_state)


@socketio.on("connect")
def handle_connect():
    """Handle client connection - send current state."""
    print("Client Connected")
    with state_lock:
        emit("state_update", {"state": current_state})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client Disconnected")


HOST = "0.0.0.0"
PORT = 3000

if __name__ == "__main__":
    activate_rpmsgtty()

    # Start the rpmsgtty monitoring thread
    monitor_thread = threading.Thread(target=monitor_rpmsgtty, daemon=True)
    monitor_thread.start()

    # Start the Flask-SocketIO server
    print(f"Starting web server on http://{HOST}:{str(PORT)}")
    socketio.run(
        app, host=HOST, port=PORT, debug=False, allow_unsafe_werkzeug=True
    )
