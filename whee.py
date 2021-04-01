import argparse
from io import TextIOWrapper, BufferedRWPair
from serial import Serial
from ursina import *
from ursina import curve, shaders

parser = argparse.ArgumentParser()

parser.add_argument("port",
    help = "the id of the port the device is on"
)

parser.add_argument("--baud", "-b",
    help    = "the device's serial baudrate",
    default = 9600
)

parser.add_argument("--delimiter", "-d",
    help    = "the csv-style delimiter",
    default = ","
)

parser.add_argument("--sample-rate", "-s",
    help = "the rate at which the device sends output (Hz)",
    default = 8000                    
)

parser.add_argument("--ready-flag", "-f",
    help    = "any unique part of the serial output string that signals the that the device is done calibrating",
    default = "pitch"
)

args = parser.parse_args()

port        = args.port
baud        = args.baud
delimiter   = args.delimiter
sample_rate = args.sample_rate
ready_flag  = args.ready_flag

sample_time = 1 / sample_rate

def serial_buffer(serial):
    return TextIOWrapper(BufferedRWPair(serial, serial))

def fallback_row(buffer, minimum_columns, last_row):
    if last_row is None:
        row = read_row(buffer, minimum_columns)
    else:
        row = last_row
    return row

def read_row(buffer, minimum_columns=0, last_row=None):
    try:
        values = buffer.readline().strip().split(delimiter)
        
        if len(values) < minimum_columns:
            row = fallback_row(buffer, minimum_columns, last_row)
        else:
            row = [float(value) for value in values]
            
        last_row = row
    except:
        row = fallback_row(buffer, minimum_columns, last_row)
    return row

serial = Serial(port, baud, timeout=sample_time)

buffer = serial_buffer(serial)
buffer.readline() # sync

class Spinner(Entity):
    def __init__(self, inactive_message, active_model, active_scale, active_color, alternate_shader, *args, **kwargs):
        self.update = self.wait
        
        self.inactive_message = Text(
            text     = inactive_message,
            origin   = (0, 0),
            position = window.center - (0, 1/5)
        )
        
        self.data_display = Text(
            text     = "ψ =    0.00     θ =    0.00     φ =    0.00",
            origin   = (0, -1),
            position = window.bottom,
            font     = "FiraMono.ttf"
        )
        
        self.active_model = active_model
        self.active_scale = active_scale
        self.active_color = active_color
        
        self.alternate_shader = alternate_shader
        
        super(Spinner, self).__init__(*args, **kwargs)
        
        self.animate_rotation(self.rotation + (0, 0, 90), 1, loop=True, curve=curve.in_out_quint)
        
    def spin(self):
        ψ_raw, θ_raw, φ_raw = read_row(buffer, 3)[0:3]
        
        ψ = -ψ_raw
        θ =  θ_raw
        φ =  φ_raw
        
        self.data_display.text = (
            "ψ = {:>7.2f}     θ = {:>7.2f}     φ = {:>7.2f}"
        ).format(ψ, θ, φ)
        
        self.animate_rotation((ψ, θ, φ), sample_time, curve=curve.in_out_sine)

    def wait(self):
        line = buffer.readline()
        if line.count(ready_flag):
            destroy(self.inactive_message)
            
            self.color = self.active_color
            self.rotation = (0, 0, 0)
            self.animate_scale(self.active_scale, 0.2, curve=curve.out_cubic)
            self.model = self.active_model
            
            self.update = self.spin
            
    def input(self, key):
        if key == 'space':
            self.shader, self.alternate_shader = self.alternate_shader, self.shader


app = Ursina()
window.color = color.black
window.fullscreen = True
window.fps_counter.enabled = False
window.borderless = False

Spinner(
    inactive_message = "calibrating—sensor must be still!",
    model            = "cube",
    active_model     = "icosphere",
    scale            = 1.5,
    active_scale     = 3,
    color            = color.red,
    active_color     = color.azure,
    shader           = shaders.lit_with_shadows_shader,
    alternate_shader = shaders.normals_shader
)

def close():
    serial.close()
    exit()

app.exitFunc = close

app.run()
