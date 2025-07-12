# live_chladni.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading

# Global state
latest_pitch = 2.0
latest_amplitude = 2.0

def chladni(x, y, n, m, A=1, B=1):
    return np.sin(n * np.pi * x) * np.sin(m * np.pi * y) + A * np.sin(m * np.pi * x) * np.sin(n * np.pi * y)

# OSC Handlers
def pitch_handler(address, *args):
    global latest_pitch
    latest_pitch = max(float(args[0]), 0.1)

def amplitude_handler(address, *args):
    global latest_amplitude
    latest_amplitude = max(float(args[0]), 0.1)

# Setup OSC server in a thread
def start_osc():
    dispatcher = Dispatcher()
    dispatcher.map("/pitch", pitch_handler)
    dispatcher.map("/amplitude", amplitude_handler)

    ip = "127.0.0.1"
    port = 9001
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print(f"Listening on {ip}:{port}...")
    server.serve_forever()

# Start OSC listener
osc_thread = threading.Thread(target=start_osc, daemon=True)
osc_thread.start()

# Create the grid
res = 512
x = np.linspace(0, 1, res)
y = np.linspace(0, 1, res)
X, Y = np.meshgrid(x, y)

# Live plotting
fig, ax = plt.subplots()
im = ax.imshow(np.zeros((res, res)), cmap='gray', interpolation='bilinear')
ax.axis('off')

def update(frame):
    global latest_pitch, latest_amplitude
    n = int(latest_pitch * 2) % 20 + 1
    m = int(latest_amplitude * 2) % 20 + 1
    Z = chladni(X, Y, n, m)
    im.set_data(Z)
    return [im]

ani = animation.FuncAnimation(fig, update, interval=100, blit=True)
plt.show()
