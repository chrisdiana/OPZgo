#!/usr/bin/python

"""

  OPZgo
  -----
  Ultra-portable backups for Teenage Engineering's OP-Z

  :usage: sudo python3 opzgo.py <optional-backup-root-location>
  :version: 0.1.1
  :copyright: 2020 Chris Diana
  :license: MIT

"""

import os
import sys
import re
import time
import usb.core
import usb.util
import shutil
import subprocess
from datetime import datetime

VENDOR = 0x2367
PRODUCT = 0x000c
USBID_OPZ = "*OP-Z_Disk*"
MOUNT_DIR = "/media/opz"
BACKUP_DIR_FORMAT = "%Y-%m-%d_%H-%M-%S"

DEFAULT_BACKUP_ROOT = "/opzgo"
BACKUP_ROOT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BACKUP_ROOT
BACKUPS_DIR = os.path.join(BACKUP_ROOT, "backups")

# OP-Z connection
def ensure_connection():
  if not is_connected():
    print("Connect your OP-Z and put it into Content Mode (Hold Track + Power)...")
    wait_for_connection()

def is_connected():
  return usb.core.find(idVendor=VENDOR, idProduct=PRODUCT) is not None

def wait_for_connection():
  try:
    while True:
      time.sleep(1)
      if is_connected():
        break
  except KeyboardInterrupt:
    sys.exit(0)

# mounting
def wait_for_mount(source, target, fs, options):
  print("Put your OP-Z into Content Mode (Hold Track + Power)...")
  try:
    while True:
      time.sleep(5)
      if mount_device(source, target, fs, options):
        break
  except KeyboardInterrupt:
    sys.exit(0)

def mount_device(source, target, fs, options=''):
  status = False
  ret = os.system('mount {} {}'.format(source, target))
  if ret == 0:
    status = True 
  return status

def unmount_device(target):
  ret = os.system('umount {}'.format(target))
  if ret != 0:
    raise RuntimeError("Error unmounting {}: {}".format(target, ret))

def eject_device(target):
  subprocess.call(["eject", target])

def get_mount_path():
  o = os.popen('readlink -f /dev/disk/by-id/' + USBID_OPZ).read()
  if USBID_OPZ in o:
    raise RuntimeError("Error getting OP-Z mount path: {}".format(o))
  else:
    return o.rstrip()

# copying
def forcedir(path):
  if not os.path.isdir(path):
    os.makedirs(path)

def backup_files(source, destination): 
  dstroot = os.path.join(destination, datetime.now().strftime(BACKUP_DIR_FORMAT))
  subprocess.call(["rsync", "-rP", source + '/', dstroot])
  blink(1)

# utils
def blink(count):
  os.system("echo none | sudo tee /sys/class/leds/led0/trigger >/dev/null 2>&1")
  for i in range(0,count):
    os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness >/dev/null 2>&1")
    time.sleep(0.15)
    os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness >/dev/null 2>&1")
    time.sleep(0.05)

def blink_long(count):
  os.system("echo none | sudo tee /sys/class/leds/led0/trigger >/dev/null 2>&1")
  os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness >/dev/null 2>&1")
  time.sleep(count)
  os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness >/dev/null 2>&1")

def blink_yay():
  os.system("echo none | sudo tee /sys/class/leds/led0/trigger >/dev/null 2>&1")
  for i in range(0,30):
    os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness >/dev/null 2>&1")
    time.sleep(0.01)
    os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness >/dev/null 2>&1")
    time.sleep(0.01)

def shutdown():
    os.system("sudo shutdown -h now")


## Main ##

# create mount point and local backup folders
blink(2)
forcedir(BACKUPS_DIR)
forcedir(MOUNT_DIR)

# wait until OP-Z is connected
print(" > Starting - waiting for OP-Z to connect")
ensure_connection()
time.sleep(5)
blink_long(3)

# mount OP-Z
mount_path = get_mount_path()
print(" > OP-Z device path: %s" % mount_path)
wait_for_mount(mount_path, MOUNT_DIR, 'ext4', 'rw')
print(" > Device mounted at %s" % MOUNT_DIR)

# copy files to local storage
blink(5)
print(" > Copying files...")
backup_files(MOUNT_DIR, BACKUPS_DIR)

# unmount OP-Z
print(" > Unmounting OP-Z")
unmount_device(MOUNT_DIR)
eject_device(mount_path)
print(" > Done.")
blink_yay()
blink_long(5)
shutdown()