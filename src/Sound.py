from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from chladni import generate_chladni

# Cache recent values
latest_pitch = 1
latest_amplitude = 1

def amplitude_handler(address, *args):
    global latest_amplitude
    latest_amplitude = max(float(args[0]), 0.01)  # avoid zero

def pitch_handler(address, *args):
    global latest_pitch, latest_amplitude
    latest_pitch = max(float(args[0]), 0.01)

    # Map values to integer range
    n = int(latest_pitch * 2)       # Scale pitch up
    m = int(latest_amplitude * 2)   # Scale amplitude

    generate_chladni(n, m)

def update(frame):
    global latest_pitch, latest_amplitude
    n = int(latest_pitch * 2) % 20 + 1
    m = int(latest_amplitude * 2) % 20 + 1
    Z = generate_chladni(n, m)
    im.set_data(Z)
    return [im]

dispatcher = Dispatcher()
dispatcher.map("/amplitude", amplitude_handler)
dispatcher.map("/pitch", pitch_handler)

ip = "127.0.0.1"
port = 9001
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"Listening on {ip}:{port}...")
server.serve_forever()
