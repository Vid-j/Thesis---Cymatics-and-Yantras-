import moderngl
import numpy as np
import glfw
import time
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading
with open("shader/fragment_shader.glsl") as f:
    fragment_shader = f.read()

with open("shader/vertex_shader.vs") as f:
    vertex_shader = f.read()

# Globals updated by OSC
latest_pitch = 2.0
latest_amplitude = 2.0

# === OSC setup ===
def pitch_handler(address, *args):
    global latest_pitch
    latest_pitch = float(args[0])

def amplitude_handler(address, *args):
    global latest_amplitude
    latest_amplitude = float(args[0])

def start_osc():
    dispatcher = Dispatcher()
    dispatcher.map("/pitch", pitch_handler)
    dispatcher.map("/amplitude", amplitude_handler)
    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9001), dispatcher)
    print("Listening for OSC...")
    server.serve_forever()

threading.Thread(target=start_osc, daemon=True).start()

# === OpenGL setup ===
if not glfw.init():
    raise Exception("GLFW failed to initialize")

win = glfw.create_window(800, 800, "Live Cymatics", None, None)
glfw.make_context_current(win)

ctx = moderngl.create_context()

prog = ctx.program(
    vertex_shader=vertex_shader,
    fragment_shader=fragment_shader # Make sure this points to the correct string
)

# Geometry
quad = np.array([
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
    -1.0,  1.0,
     1.0, -1.0,
     1.0,  1.0,
], dtype='f4')

vbo = ctx.buffer(quad.tobytes())
vao = ctx.simple_vertex_array(prog, vbo, "in_vert")
# start_time = time.time()
# === Render loop ===
while not glfw.window_should_close(win):
    glfw.poll_events()

    # Update uniforms from live values
    prog["pitch"].value = max(1.0, min(latest_pitch * 2, 20.0))
    prog["amplitude"].value = max(1.0, min(latest_amplitude * 2, 20.0))


    ctx.clear(0.0, 0.0, 0.0)
    vao.render()
    glfw.swap_buffers(win)

glfw.terminate()
