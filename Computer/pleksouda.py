import PySimpleGUI as sg
from pysinewave import SineWave
import serial
from time import sleep
import random

"""PyAudio PySimpleGUI Non Blocking Stream for Microphone"""

# VARS CONSTS:
_VARS = {'window': False,
         'stream': False,
         'initial_pitch': -7,
         'min_pitch': -15,
         'max_pitch': 2,
         'decibels_per_second': 100,
         'pitch_per_second': 10,
         'port': 8,
         'usb_max': 255}

# pysimpleGUI INIT:
AppFont = 'Any 16'
sg.theme('DarkTeal2')
layout = [[[sg.Text('Initial Pitch'), sg.InputText(_VARS['initial_pitch'], key='InitPitch', disabled=True, enable_events=True)],
           [sg.Text('Max Pitch'), sg.InputText(_VARS['max_pitch'], key='MaxPitch', disabled=True, enable_events=True)],
           [sg.Text('Min Pitch'), sg.InputText(_VARS['min_pitch'], key='MinPitch', disabled=True, enable_events=True)],
           [sg.Text('Pitch Per Second'), sg.InputText(_VARS['pitch_per_second'], key='PitchPerSec', disabled=True, enable_events=True)],
           [sg.Text('Serial Port'), sg.InputText(_VARS['port'], key='Port', disabled=True, enable_events=True)],
           [sg.Text('USB Max value'), sg.InputText(_VARS['usb_max'], key='UsbMax', disabled=True, enable_events=True)]],
          [sg.Button('Save', font=AppFont, disabled=True)],
          [sg.Text('Frequency Playing (LOW<- | HIGH->):', key='FrequencyMessage', visible=False), sg.ProgressBar(100, orientation='h', size=(20, 20), key='Frequency', visible=False)],
          [sg.Text('Enter pitch'), sg.InputText(_VARS['initial_pitch'], key='Pitch', disabled=True, enable_events=True),
           sg.Button('Set', font=AppFont, disabled=True),
           sg.Slider(key='Volume', range=(0, 100), disabled=True, orientation='v', size=(10, 15), default_value=100, enable_events = True)],
          [sg.Button('Play-USB', font=AppFont),
           sg.Button('Play-Random', font=AppFont),
           sg.Button('Play', font=AppFont),
           sg.Button('Stop', font=AppFont, disabled=True),
           sg.Button('Exit', font=AppFont),
           sg.Button('Calibrate', font=AppFont, disabled=False)]]
_VARS['window'] = sg.Window('Instrument | Pleksouda', layout, finalize=True)


# FUNCTIONS:

def stop():
    print('Stopped playback')
    if _VARS['stream']:
        _VARS['window']['FrequencyMessage'].update(visible=False)
        _VARS['window']['Frequency'].update(0, visible=False)
        _VARS['window']['Stop'].Update(disabled=True)
        _VARS['window']['Play'].Update(disabled=False)
        _VARS['window']['Play-USB'].Update(disabled=False)
        _VARS['window']['Play-Random'].Update(disabled=False)
        _VARS['window']['Set'].Update(disabled=True)
        _VARS['window']['Volume'].Update(disabled=True)
        _VARS['window']['Pitch'].Update(disabled=True)
        _VARS['window']['Calibrate'].Update(disabled=False)
        _VARS['stream'].stop()
        _VARS['stream'] = False


def play():
    print('Entering manual playback')
    _VARS['window']['Stop'].Update(disabled=False)
    _VARS['window']['Play'].Update(disabled=True)
    _VARS['window']['Play-USB'].Update(disabled=True)
    _VARS['window']['Play-Random'].Update(disabled=True)
    _VARS['window']['Set'].Update(disabled=False)
    _VARS['window']['Volume'].Update(disabled=False)
    _VARS['window']['Pitch'].Update(disabled=False)
    _VARS['window']['Calibrate'].Update(disabled=True)
    # Turn the sine wave on.
    _VARS['stream'] = SineWave(pitch=_VARS['initial_pitch'], pitch_per_second=_VARS['pitch_per_second'], decibels_per_second=_VARS['decibels_per_second'])
    _VARS['stream'].play()
    set_pitch()


def play_random():
    print('Entering random playback')
    _VARS['window']['Stop'].Update(disabled=False)
    _VARS['window']['Play'].Update(disabled=True)
    _VARS['window']['Play-USB'].Update(disabled=True)
    _VARS['window']['Play-Random'].Update(disabled=True)
    _VARS['window']['Exit'].Update(disabled=True)
    _VARS['window']['Set'].Update(disabled=True)
    _VARS['window']['Volume'].Update(disabled=False)
    _VARS['window']['Pitch'].Update(disabled=True)
    _VARS['window']['Calibrate'].Update(disabled=True)
    # Turn the sine wave on.
    _VARS['stream'] = SineWave(pitch=_VARS['initial_pitch'], pitch_per_second=_VARS['pitch_per_second'], decibels_per_second=_VARS['decibels_per_second'])
    _VARS['stream'].play()

    while True:
        # Check for Events
        event, values = _VARS['window'].read(timeout=200)
        if event == 'Stop':
            stop()
            _VARS['window']['Exit'].Update(disabled=False)
            break
        if event == 'Volume':
            set_volume(float(values['Volume'] - 100))
        randomness = random.randrange(_VARS['min_pitch'], _VARS['max_pitch'], 1)
        print("Playing Pitch: ", randomness)
        set_pitch(randomness)
        sleep(2)


def set_pitch(pitch=_VARS['initial_pitch']):
    _VARS['window']['FrequencyMessage'].update(visible=True)
    percentage = 100*(pitch-_VARS['min_pitch'])/(_VARS['max_pitch']-_VARS['min_pitch'])
    _VARS['window']['Frequency'].update(percentage, visible=True)
    _VARS['stream'].set_pitch(pitch)


def set_volume(volume):
    if _VARS['stream']:
        _VARS['stream'].set_volume(volume)


def calibrate():
    print('Calibration')
    if not _VARS['stream']:
        # Buttons
        _VARS['window']['Stop'].Update(disabled=True)
        _VARS['window']['Play'].Update(disabled=True)
        _VARS['window']['Play-USB'].Update(disabled=True)
        _VARS['window']['Play-Random'].Update(disabled=True)
        _VARS['window']['Set'].Update(disabled=True)
        _VARS['window']['Volume'].Update(disabled=True)
        _VARS['window']['Save'].Update(disabled=False)
        _VARS['window']['Calibrate'].Update(disabled=True)
        # Inputs
        _VARS['window']['InitPitch'].Update(disabled=False)
        _VARS['window']['MaxPitch'].Update(disabled=False)
        _VARS['window']['MinPitch'].Update(disabled=False)
        _VARS['window']['PitchPerSec'].Update(disabled=False)
        _VARS['window']['Port'].Update(disabled=False)
        _VARS['window']['UsbMax'].Update(disabled=False)


def save(initial_pitch, max_pitch, min_pitch, pitch_per_second, port, usb_max):
    print('Saved Configuration')
    # Buttons
    _VARS['window']['Play'].Update(disabled=False)
    _VARS['window']['Play-USB'].Update(disabled=False)
    _VARS['window']['Play-Random'].Update(disabled=False)
    _VARS['window']['Calibrate'].Update(disabled=False)
    _VARS['window']['Save'].Update(disabled=True)
    # Inputs
    _VARS['window']['InitPitch'].Update(disabled=True)
    _VARS['window']['MaxPitch'].Update(disabled=True)
    _VARS['window']['MinPitch'].Update(disabled=True)
    _VARS['window']['PitchPerSec'].Update(disabled=True)
    _VARS['window']['Port'].Update(disabled=True)
    _VARS['window']['UsbMax'].Update(disabled=True)
    # Save vars
    _VARS['window']['Pitch'].update(initial_pitch)
    _VARS['initial_pitch'] = initial_pitch
    _VARS['max_pitch'] = max_pitch
    _VARS['min_pitch'] = min_pitch
    _VARS['pitch_per_second'] = pitch_per_second
    _VARS['port'] = port
    _VARS['usb_max'] = usb_max


def play_usb(serial_port):
    print('Entering USB playback')
    _VARS['window']['Stop'].Update(disabled=False)
    _VARS['window']['Play'].Update(disabled=True)
    _VARS['window']['Play-USB'].Update(disabled=True)
    _VARS['window']['Play-Random'].Update(disabled=True)
    _VARS['window']['Set'].Update(disabled=True)
    _VARS['window']['Volume'].Update(disabled=False)
    _VARS['window']['Pitch'].Update(disabled=True)
    _VARS['window']['Calibrate'].Update(disabled=True)
    _VARS['window']['Exit'].Update(disabled=True)
    # Turn the sine wave on.
    _VARS['stream'] = SineWave(pitch=_VARS['initial_pitch'], pitch_per_second=_VARS['pitch_per_second'], decibels_per_second=_VARS['decibels_per_second'])
    _VARS['stream'].play()

    # Initialize incoming value
    usb = (_VARS['initial_pitch']+abs(_VARS['min_pitch']))*_VARS['usb_max']/(_VARS['max_pitch']-_VARS['min_pitch'])
    while True:
        # Check for Events
        event, values = _VARS['window'].read(timeout=200)
        if event == 'Stop':
            stop()
            _VARS['window']['Exit'].Update(disabled=False)
            #close serial
            serial_port.close()
            break
        if event == 'Volume':
            set_volume(float(values['Volume'] - 100))

        # Obtain USB value
        if serial_port.in_waiting:
            usb = serial_port.readline()
            if usb > _VARS['usb_max']:
                usb = _VARS['usb_max']
            if usb < 0:
                usb = 0
            # print(usb)

        # Process USB value
        usb = int(usb)
        usb_pitch = (usb/_VARS['usb_max'])*(_VARS['max_pitch']-_VARS['min_pitch'])-abs(_VARS['min_pitch'])
        print("USB said: ",usb, '- Playing Pitch: ', usb_pitch)
        set_pitch(usb_pitch)
        sleep(1)

# MAIN LOOP

while True:
    event, values = _VARS['window'].read(timeout=200)
    # Exit
    if event == sg.WIN_CLOSED or event == 'Exit':
        stop()
        break
    # Buttons
    if event == 'Stop':
        stop()
    if event == 'Play':
        play()
    if event == 'Play-Random':
        play_random()
    if event == 'Set':
        set_pitch(float(values['Pitch']))
    if event == 'Volume':
        set_volume(float(values['Volume']-100))
    if event == 'Calibrate':
        calibrate()
    if event == 'Save':
        save(float(values['InitPitch']), float(values['MaxPitch']), float(values['MinPitch']), float(values['PitchPerSec']), int(values['Port']), int(values['UsbMax']))
    if event == 'Play-USB':
        serial_port = serial.Serial(
            port='COM'+str(_VARS['port']), \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=0)
        play_usb(serial_port)
    # Input validation
    if event == 'Pitch'and values['Pitch'] and values['Pitch'][-1] not in ('0123456789.-'):
        _VARS['window']['Pitch'].update(values['Pitch'][:-1])
    if event == 'InitPitch' and values['InitPitch'] and values['InitPitch'][-1] not in ('0123456789.-'):
        _VARS['window']['InitPitch'].update(values['InitPitch'][:-1])
    if event == 'MaxPitch' and values['MaxPitch'] and values['MaxPitch'][-1] not in ('0123456789.-'):
        _VARS['window']['MaxPitch'].update(values['MaxPitch'][:-1])
    if event == 'MinPitch' and values['MinPitch'] and values['MinPitch'][-1] not in ('0123456789.-'):
        _VARS['window']['MinPitch'].update(values['MinPitch'][:-1])
    if event == 'PitchPerSec' and values['PitchPerSec'] and values['PitchPerSec'][-1] not in ('0123456789.-'):
        _VARS['window']['PitchPerSec'].update(values['PitchPerSec'][:-1])
    if event == 'UsbMax' and values['UsbMax'] and values['UsbMax'][-1] not in ('0123456789.-'):
        _VARS['window']['UsbMax'].update(values['UsbMax'][:-1])
    if event == 'Port' and values['Port'] and values['Port'][-1] not in ('0123456789'):
        _VARS['window']['Port'].update(values['Port'][:-1])

_VARS['window'].close()
