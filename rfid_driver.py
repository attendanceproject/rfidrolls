#!/usr/bin/python
import sys

import usb.core
import usb.util
from time import sleep

# find USB RFID reader
dev = usb.core.find(idVendor=0x0c27, idProduct=0x3bfa)

# was it found?
if dev is None:
  print 'device not found'
# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# if the OS kernel already claimed the device, which is most likely true
if dev.is_kernel_driver_active(interface) is True:
  # tell the kernel to detach
  dev.detach_kernel_driver(interface)
  # claim the device
  usb.util.claim_interface(dev, interface)

collected = 0
full_read = 14 #full read of usb endpoint
rfid = ""
try:
  #while collected < attempts :
  while 1 == 1 :
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        collected += 1
        #print data
        #Is not ASCII so need to modify manually
        if (data[2] > 29) and (data[2] < 40) :
          if data[2] == 39:
            rfid += '0'
          else:
            rfid += str(data[2] - 29)
        #If enter key read one more byte and send rfid number
        if (data[2] == 40) and (collected > 1):
          data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
          collected = 0
          print 'RFID: ' + rfid
          rfid = ""
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue

except KeyboardInterrupt:
  # release the device
  usb.util.release_interface(dev, interface)
  # reattach the device to the OS kernel
  dev.attach_kernel_driver(interface)
  print 'Usb device released and reattached to OS kernel'