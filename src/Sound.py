# This file is part of the SoundOSC project.
# it receives OSC messages from MaxMsp and prints the amplitude value.

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

def amplitude_handler(address, *args):
    value = args[0]
    print(f"Amplitude: {value:.3f}")
    # Use this value to drive your Chladni pattern

dispatcher = Dispatcher()
dispatcher.map("/amplitude", amplitude_handler)

ip = "127.0.0.1"
port = 9000
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)

print(f"Listening on {ip}:{port}...")
server.serve_forever()
