# Instrument Pleksouda

A Theremin like instrument, based on a Computer-Microcontoler interface. The microcontroler caclulates and sends the sensor context to the Computer via the USB serial port. 

## Implementation

### Computer

In this implementation, the Computer side is a Python project with a GUI that allows to:
- Calibrate configuration (initial pitch, pitch range, incoming max value, serial port number, pitch change velocity)
- Control the playback volume
- Play manually certain frequencies
- Play random frequencies
- Play incoming values from the USB port


### Microcontroller

In this implementation, the Microcontroller side is an Arduino project combining a set of distance sensors, in order to provide continuous feedback into the Serial Port. 


### Modularity

Both implementations are independent of each other, offering maximum modularity. The computer side project is capable to work after calibration with any kind of incoming serial data. Same way, the microcontroller side could feed any type of computer software, able to digest the serial data. 

## Build and run

You will need to install pyinstaller using:
```commandline
pip3 install pyinstaller
```
Now, into the file plekosuda.spec, edit the field "pathex" to map into the path you stored the project. Then, from within the Computer folder run in Terminal:
```
pyinstaller --onefile -w pleksouda.spec
```

In order to run the project, afterwards just double click the executable found under ```Path/Computer/dist```.

Of course, you can always avoid build and run the project from within a Python Interpreter using (within the Computer path):
```commandline
python3 pleksouda.py
```

### Notices

- If you are using windows, you may need to add the exe file as an exception in your Antivirus.
- If you are using windows, you may have to run the exe file as an administrator.
- Before selecting the USB playback module, ensure that the microcontroller is already sending data to the proper Serial port.
- Before selecting the USB playback module you have to ensure that you don't have any open terminal on the Serial port. This could block the app from using the Serial port to read.