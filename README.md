# whee

An interactive visualization using an MPU-6050's gyroscope data as recorded by an Arduino.

## requirements

This won't work with Python 3.9! This has only been tested successfully on Python 3.8, but earlier versions may or may not work. 

To make things easier, ensure Python is [in your PATH](https://datatofish.com/add-python-to-windows-path/).

## setup

Clone or download and unzip this repository. Then, navigate to the project's root directory in a terminal.

This might be something like:

```shell
cd ~/Downloads/whee
```

I recommend starting setup by making a virtual environment.

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

The following command runs the visualization:

```shell
python whee.py [-h] [--baud BAUD] [--delimiter DELIMITER] [--sample-rate SAMPLE_RATE] [--ready-flag READY_FLAG] port
```

You can easily find the Arduino's port using PlatformIO.

```shell
pio device list
```

During the visualization, hit the spacebar to switch from shadows to normals.

### example - windows

```powershell
python whee.py COM5
```

## editing

The visualization Python source is just `/whee.py`. I kept as much of the more IO-focused code as general as possible, and the [Ursina](https://www.ursinaengine.org/) graphics engine is a joy to use. Have fun!

The Arduino source can be found at `/src/main.ino`. There, you can change outputs from the Arduino. Open it with any editor and build or compile with PlatformIO (or even with the integrated VS Code extension). Alternatively, open it in the Arduino IDE (which will ask you to move it to a new folder). As currently configured, the Arduino's outputs work well with the serial plotter.
