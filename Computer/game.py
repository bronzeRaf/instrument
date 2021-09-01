import PySimpleGUI as sg
import pyaudio
import numpy as np
from pysinewave import SineWave

"""PyAudio PySimpleGUI Non Blocking Stream for Microphone"""

# VARS CONSTS:
_VARS = {'window': False,
         'stream': False}

# pysimpleGUI INIT:
AppFont = 'Any 16'
sg.theme('DarkTeal2')
layout = [[sg.ProgressBar(4000, orientation='h',
                          size=(20, 20), key='-PROG-')],
          [sg.Text('Enter pitch'), sg.InputText(),
           sg.Button('Set', font=AppFont, disabled=True)
           ],
          [sg.Button('Listen', font=AppFont),
           sg.Button('Play', font=AppFont),
           sg.Button('Stop', font=AppFont, disabled=True),
           sg.Button('Exit', font=AppFont)]]
_VARS['window'] = sg.Window('Microphone Level', layout, finalize=True)

# PyAudio INIT:
CHUNK = 1024  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 1  # Sampling Interval in Seconds ie Interval to listen

pAud = pyaudio.PyAudio()


# FUNCTIONS:


def stop(sinewave):
    if _VARS['stream']:
        _VARS['stream'].stop_stream()
        _VARS['stream'].close()
        _VARS['window']['-PROG-'].update(0)
        _VARS['window'].FindElement('Stop').Update(disabled=True)
        _VARS['window'].FindElement('Listen').Update(disabled=False)
        _VARS['window'].FindElement('Play').Update(disabled=False)
        _VARS['window'].FindElement('Set').Update(disabled=True)
        sinewave.stop()


def callback(in_data, frame_count, time_info, status):
    # print(in_data)
    data = np.frombuffer(in_data, dtype=np.int16)
    # print(np.amax(data))
    _VARS['window']['-PROG-'].update(np.amax(data))
    return (in_data, pyaudio.paContinue)


def play_callback(in_data, frame_count, time_info, status):
    # print(in_data)
    X1 = np.linspace(0, 5 * np.pi, num=441, endpoint=False)
    Y1 = (5000 * np.sin(X1)).astype(np.int16)
    data = Y1.tobytes()
    data = np.frombuffer(in_data, dtype=np.int16).to_bytes()
    # print(np.amax(data))
    # _VARS['window']['-PROG-'].update(np.amax(data))
    return (data, pyaudio.paContinue)


def listen():
    _VARS['window'].FindElement('Stop').Update(disabled=False)
    _VARS['window'].FindElement('Listen').Update(disabled=True)
    _VARS['window'].FindElement('Play').Update(disabled=True)
    _VARS['stream'] = pAud.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK,
                                stream_callback=callback)

    _VARS['stream'].start_stream()


def play(sinewave):
    _VARS['window'].FindElement('Stop').Update(disabled=False)
    _VARS['window'].FindElement('Listen').Update(disabled=True)
    _VARS['window'].FindElement('Play').Update(disabled=True)
    _VARS['window'].FindElement('Set').Update(disabled=False)
    # Turn the sine wave on.
    sinewave.play()


def set(sinewave, pitch):
    _VARS['window'].FindElement('Stop').Update(disabled=False)
    _VARS['window'].FindElement('Listen').Update(disabled=True)
    _VARS['window'].FindElement('Play').Update(disabled=True)
    sinewave.set_pitch(pitch)


# MAIN LOOP
sinewave = SineWave(pitch=0)
while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == sg.WIN_CLOSED or event == 'Exit':
        stop()
        pAud.terminate()
        break
    if event == 'Listen':
        listen()
        print("still")
    if event == 'Stop':
        stop(sinewave)
    if event == 'Play':
        play(sinewave)
    if event == 'Set':
        set(sinewave, int(values[0]))

_VARS['window'].close()
