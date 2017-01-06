#!/usr/bin/env python

import serial

def pl2303_open(device="/dev/ttyUSB0"):
    return serial.Serial(device, 9600)

if __name__ == "__main__":
    print '"close all the doors and electrical equipments"'
   
    pl2303 = pl2303_open()

    v = "C"
        pl2303.write(v)
        print 'PI: %s'%(v)
