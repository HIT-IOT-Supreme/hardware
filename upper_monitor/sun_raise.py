#!/usr/bin/env python

import serial

def pl2303_open(device="/dev/ttyUSB0"):
    return serial.Serial(device, 9600)

if __name__ == "__main__":
    print '"Now the clock is beginning~"'
   
    pl2303 = pl2303_open()

    v = "H"
        pl2303.write(v)
        print 'PI: %s'%(v)
