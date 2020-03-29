# OPZgo

>Ultra-portable backups for Teenage Engineering's OP-Z

![OPZgo running on Raspberry Pi Zero](https://i.imgur.com/aqGDum8.jpg)

Inspired by [tacoe's OP1GO](https://github.com/tacoe/OP1GO), this small script allows for full OP-Z backups while on the go using a Raspberry Pi Zero W. Simply plug your OP-Z into the Pi Zero and it will automatically create a timestamped full backup of your OP-Z including any projects, sample packs, bounces and configurations.

### What's needed

* OP-Z
* Raspberry Pi Zero W
* Micro SD Card (at least 4GB)
* USB-C to USB micro cable
* USB-A to USB micro cable (for power)
* Power source (i.e. power adapter, power bank)


## Usage

1. Plug in your Pi to a power source and wait for it to boot up (the green LED should stop blinking once fully booted).
2. Plug in your OP-Z first (powered off) and wait for a long blink indicating the OP-Z is recognized.
3. Now that everything is ready, put your OP-Z into [Content Mode](https://teenage.engineering/guides/op-z/disk-modes) by holding the Track button while turning on the unit.
4. The Pi's LED will then blink 5 times indicating the backup process has begun. During the backup process, the Pi's LED will blink rapidly. 
5. Once finished, the LED will long blink for 5 seconds to signal the backup has completed. The OP-Z will be automatically unmounted and ejected. You should see the OP-Z reboot into normal mode. 
6. Wait 5 seconds after that long LED blink and the Pi should do a couple more blinks indicating it is shutting down gracefully.  
7. Once you see no more LED blinks the Pi has safely shut down. It's now safe to disconnect the OP-Z and unplug the Pi.


## Setup 

**Quick Start:**

1. Download the [latest OPZgo image here](https://mega.nz/#!KpVTlQKA!0iSO4_0hDjeTeQvDeuK2WALMTdKEfOoMUL8eYqAzXQE).
2. Flash to a SD card using [Etcher](https://www.balena.io/etcher/).
3. Plug it into your Raspberry Pi and you're ready to start making backups!

**Manual Setup:**

If you wish to manually install it yourself, check out the [instructions here](https://github.com/chrisdiana/OPZgo/wiki/Manual-Setup).


## Accessing Backups

You can access backups by plugging the SD card into a computer. You should see a disk called `BOOT`. Within `BOOT` all backups are saved to `opzgo/backups/` as timestamped directories each time you trigger a backup. 


### Troubleshooting & a few things to note

* Sometimes the OP-Z will fail to connect or mount. If after a long time (>5 minutes) you still don't see the series of LED patterns described above, do NOT assume the backup was successful. Try unplugging the power from the Pi, reboot and try again.

* The script will only backup once per boot so if you want to backup again you will have to restart the process.

* This software is provided "as is", without warranty. 
