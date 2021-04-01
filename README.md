# whee

An interactive visualization using an MPU-6050's gyroscope data as recorded by an Arduino.

## requirements

This won't work with Python 3.9! This has only been tested successfully on Python 3.8, but earlier versions may or may not work. 

To make things easier, ensure Python is [in your PATH]([How to add Python to Windows PATH - Data to Fish](https://datatofish.com/add-python-to-windows-path/)).

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


