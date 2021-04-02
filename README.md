# whee.py

An interactive visualization using an GY-521's gyroscope data as recorded by an Arduino.

![demo gif](https://user-images.githubusercontent.com/20602415/113386208-9743f200-933e-11eb-86b8-3006353eb8ab.gif "demo gif")

*A sample of the visualization.*

## requirements

This won't work with Python 3.9! This has only been tested successfully on Python 3.8; earlier versions may or may not work. To make things easier, ensure Python is [in your PATH](https://datatofish.com/add-python-to-windows-path/).

## setup

Clone or download and unzip this repository.

Then, navigate to the project's root directory in a terminal. If you've decided to keep the folder in your downloads, this might be something like:

```shell
cd ~/Downloads/whee
```

I recommend starting setup by making a virtual environment for Python installs. This helps avoid conflicts with other Python software.

```shell
python -m venv env
./env/Scripts/activate
```

Then, install the Python dependencies.

```shell
pip install -r requirements.txt
```

Upload the Arduino code to the board using the PlatformIO Python module. This can be easier for a project like this than using the Arduino IDE. Any unmet dependencies will be installed automatically the first time this is run.

```shell
pio run -t upload
```

## use

Wire up the sensor to the Arduino [like this](https://create.arduino.cc/projecthub/Nicholas_N/how-to-use-the-accelerometer-gyroscope-gy-521-6dfc19).

When you open a new terminal session, be sure to activate the virtual environment before using the program.

```shell
./env/Scripts/activate
```

A command in the following form runs the visualization:

```shell
whee.py [-h] [--port PORT] [--baud BAUD] [--delimiter DELIMITER] [--sample-rate SAMPLE_RATE] [--ready-flag READY_FLAG]
```

Use the `-h` option to see more info on each item.

Keep the sensor steady until the program indicates that calibration has ended. During the visualization, hit the spacebar to switch coloring from shadows to normals.

If calibration seems to go on forever, try hitting the reset button on the Arduino. Sometimes the serial interface isn't the most stable, so data like the *ready* flag can get lost.

### examples

To use default settings and let the program guess the right port (this should work in many cases):

```shell
python whee.py
```

To tell the program you want Windows port COM5 and a baudrate of 4800:

```powershell
python whee.py -p COM5 -b 4800
```

#### finding the arduino's port

You can find the Arduino's port yourself using your system's device manager, the Arduino IDE, or PlatformIO:

```shell
pio device list
```

## editing & debugging

The visualization Python source is just `/whee.py`. I kept as much of the more IO-focused code as general as possible, and the [Ursina](https://www.ursinaengine.org/) graphics engine is a joy to use. Have fun!

The Arduino source can be found at `/src/main.ino`. There, you can change outputs from the Arduino. Open it with your favorite editor and build or compile with PlatformIO. You can even install the [PlatformIO extension](https://platformio.org/install/integration) for your editor! Alternatively, you can open the file in the Arduino IDE, which will have you move it to a new folder and break the current PlatformIO setup.

For debugging, the Arduino code's preconfigured outputs work well with the Arduino serial plotter. This is convenient for people using the Arduino IDE, but people using other editors and PlatformIO can also use the serial plotter without opening the code in the Arduino IDE.

![plotter gif](https://user-images.githubusercontent.com/20602415/113387906-0e2eba00-9342-11eb-9f0d-9ebf5e8c6310.gif "plotter gif")

*Data shown in the serial plotter.*
