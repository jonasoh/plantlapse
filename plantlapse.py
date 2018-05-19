#!/usr/bin/env python3
#

from picamera import PiCamera
from optparse import OptionParser
import time
import sys

version = "0.1.0"

parser = OptionParser(version="plantlapse " + version)

parser.add_option('-n', '--num-shots', default=168, type="int", dest="nshots",
                    help="number of shots to capture [default: 168]")
parser.add_option('-d', '--delay', type="float", default=60, dest="delay", 
                    help="time to wait between shots [default: 60]")
parser.add_option('--day-shutter', default=50, dest="dayshutter", type="int", 
                    help="daytime shutter in fractions of a second, i.e. for 1/100 specify '100' [default: 50]")
parser.add_option('--night-shutter', default=200, dest="nightshutter", type="int", 
                    help="nighttime shutter in fractions of a second [default: 200]")
parser.add_option('--day-iso', default=100, dest="dayiso", type="int",
                    help="set daytime ISO value (0=auto) [default: 100]")
parser.add_option('--night-iso', default=100, dest="nightiso", type="int",
                    help="set nighttime ISO value (0=auto) [default: 100]")
parser.add_option('-r', '--resolution', default="2592x1944", dest="resolution", 
                    help="set camera resolution [default: 2592x1944]")
parser.add_option('--prefix', default="", dest="prefix", 
                    help="prefix to use for filenames [default: none]")
parser.add_option('--auto-wb', default=False, action="store_true", dest="awb",
                    help="adjust white balance between shots (if false, only adjust when day/night shift is detected) [default: false]")
parser.add_option('--preview', action="store_true", default=False, dest="preview",
                    help="show a live preview of the current settings for 60 seconds, then exit")

(options, args) = parser.parse_args()

def initCam():
    cam = PiCamera()
    cam.resolution=options.resolution 
    cam.meter_mode='spot'
    cam.led=False
    return cam

def isDaytime():
    # determine if it's day or not. give the camera 1 second to adjust.
    oldshutter=cam.shutter_speed
    oldiso=cam.iso
    cam.shutter_speed=0
    cam.iso = 100
    time.sleep(1)
    exp = cam.exposure_speed
    print("Exposure speed: %f" % exp)
    if exp < 20000:
        day=True
    else:
        day=False
    cam.shutter_speed=oldshutter
    cam.iso=oldiso
    return day

def setWB():
    sys.stdout.write("Determining white balance")
    cam.awb_mode='auto'
    (one, two) = cam.awb_gains
    sys.stdout.flush()
    for i in range(1,5):
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()
    print(" done.")
    cam.awb_mode="off"
    cam.awb_gains = (one, two)

cam=initCam()
daytime="TBD"

if options.preview:
    cam.start_preview()
    sleep(60)
    cam.stop_preview()
    sys.exit()

for n in range(0, options.nshots):
    prev_daytime=daytime
    daytime=isDaytime()
    
    # set new wb if there's a day/night shift
    if prev_daytime != daytime:
        if not options.awb:
            setWB()

    if daytime:
        cam.shutter_speed=1000000//options.dayshutter
        cam.iso=options.dayiso
    else:
        cam.shutter_speed=1000000//options.nightshutter
        cam.iso=options.nightiso
    
    now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    filename = options.prefix + now + ".jpg"
    sys.stdout.write("Capturing %s..." % filename)
    sys.stdout.flush()
    cam.capture(filename)

    if daytime:
        print(" daytime picture captured OK.")
    else:
        print(" nighttime picture captured OK.")

    time.sleep(options.delay*60)
