# SPIRO is a Smart Plate Imaging Robot
SPIRO is a Raspberry Pi based imaging platform designed for highly reproducible, high temporal resolution timelapse imaging of biological samples grown on Petri dishes: plant seedlings, fungal mycelium, bacterial colonies etc.

SPIRO supports imaging of up to four plates at the same time. It is designed it to be suitable for the two most poular Petri dish formats: round 9 cm plates and square 12 cm plates.

## Hardware

SPIRO is based around [Raspberry Pi 3 B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/), using 3D printed parts to hold everything together. It works with both the [official camera module](https://www.raspberrypi.org/products/camera-module-v2/) as well as with third-party cameras. We use the [Arducam Motorized Focus camera](http://www.arducam.com/programmable-motorized-focus-camera-raspberry-pi/), which allows focusing the images via the built-in live view web server.

The image below is a link to a YouTube video showing some of its design and features.

[![SPIRO intro](https://user-images.githubusercontent.com/6480370/60589568-1e46ed80-9d9a-11e9-96ae-08fe85d8b415.png)](http://www.youtube.com/watch?v=fh5NMvDNjNc "SPIRO intro")

## 3D printer models

Models for the 3D printed hardware components can be found at [AlyonaMinina/SPIRO](https://github.com/AlyonaMinina/SPIRO).

## ImageJ macros

A few ImageJ macros that take advantage of the capabilities of SPIRO can be found at [jiaxuanleong/spiro-IJmacros](https://github.com/jiaxuanleong/spiro-IJmacros).

## Installation

First, prepare the SD card with a fresh release of Raspbian Lite (follow the official [instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)). 

Connect the Raspberry Pi to a screen and keyboard. Log in using the default credentials (username `pi`, password `raspberry`). Start the system configuration:
```
sudo raspi-config
```

In the raspi-config interface, make the following changes:
* Change the password
* Under *Interfacing*, enable *Camera*, *I2C*, and *SSH*. 
* In the *Advanced Options*, set *Memory Split* to 256.
* Under *Localisation Options*, make sure to set the *Timezone*. Please note that a working network connection is required to maintain the correct date.
* If needed, configure *Network* and *Localization* options here as well.
* Finally, select *Finish*, and choose to reboot the system when asked. 

Next, make sure the system is up to date, and install the required tools (answer yes to any questions):

```
sudo apt update
sudo apt upgrade
sudo apt install python3-pip git
```

Finally, install the SPIRO software and its dependencies:

```
sudo pip3 install git+https://github.com/jonasoh/spiro#egg=spiro
```

You may now run the spiro software using the command
```
spiro
```

## Usage

### Working with SPIRO

To issue commands to SPIRO, and to download the images, you need an SSH client. Depending on your operating system and how comfortable you are with a computer, there are several choices.

**Windows**
* [MobaXterm](https://mobaxterm.mobatek.net/) is a popular SSH client that also supports file transfer. Recommended for beginners. 
* [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) is a lightweight and popular SSH client.
* [WinSCP](https://winscp.net/eng/index.php) can be used to transfer files from SPIRO using the SFTP protocol.

**Mac**
* On Mac, an SSH client is built in to the system. Using the *Terminal*, connect to SPIRO using the command `ssh pi@1.2.3.4` (where `1.2.3.4` is the IP address of your system). Images can be transferred using the builtin commands `scp` and `sftp`, although this requires some knowledge about using the command line.
* [Transmit](https://panic.com/transmit/) is the best graphical SFTP client for Mac.
* [Cyberduck](https://cyberduck.io/) may be another alternative.
