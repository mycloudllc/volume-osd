This project was built to be used with [OpenDSH](https://github.com/openDsh/dash). It should work standalone, but mileage will vary.

Installation:
 To use this python script, dunst needs to be installed. Install by running:
 ```
 sudo apt install dunst libnotify-bin
 ```
 To be able to use the rotary encoder, some software is needed for the gpio.
 Install with:
 ```
 sudo apt install python3-gpiozero
 ```
 Once those are installed you will need to replace the dunstrc file in  ```/etc/xdg/dunst``` with the one in this repo. This file can be customized to fit your needs and customize further. Documenation can be found [here](https://dunst-project.org/documentation/).
```
cd volume-osd
mv /etc/xdg/dunst/dunstrc dunstrc_backup
cp dunstrc /etc/xdg/dunst/dunstrc
```
 Next we will need to place some icons in the default icon location for Raspberry OS.
```
sudo mkdir /usr/share/icons/Volume
sudo cp volume-up.png /usr/share/icons/Volume/volume-up.png
sudo cp volume-down.png /usr/share/icons/Volume/volume-down.png
sudo cp muted.png /usr/share/icons/Volume/muted.png
```
You MUST reboot after all changes have been made. The script can be ran 2 ways, manually, or at boot.

To run manually:
```
python3 dunst_vol_not.py
```
To run at start run:
```
sudo nano /etc/rc.local
```
Add the following ```sudo python3 /home/pi/volume-osd/dunst_vol_not.py &``` and press Ctrl+O then Crtl+X and reboot the pi.

