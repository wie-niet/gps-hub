# gps-hub
Garmin USB web hub. Upload gpx files to your USB Garmin GPS device from your smartphone.
Install this web deamon on a Raspberry pi and you can acces your old fashion USB GPS on the go.

This deamon has been created for the eTrex 30 model, it uses the GarminDevice.xml file to find the "UserDataSync" folder. 

Warning: this service has no additional security features. As long you are the only one with network access to this server there is no problem. Everyone who can access this the webserver will have the ability to access your GPS and bring the system t halt. And using the debug feature it may have full control to your Raspberry pi.

# Install 
  
## clone or extract files into /opt/gps-hub
```
cd /opt && git clone https://github.com/wie-niet/gps-hub.git
```


## Install systemd.service
```
cd /opt/gps-hub
cp systemd.gps-hub.service /etc/systemd/system/gps-hub.servic
chmod 644 /etc/systemd/system/gps-hub.service
systemctl daemon-reload
systemctl enable gps-hub
```

# Prepare for the on the road
1. setup your cellphone as hotspot.  
2. setup your Raspberry pi to connect with your hotspot. (https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
3. make sure your Garmin GPS has disk label "GARMIN"
4. remember the hostname of your Raspberry pi, you need it on the road.

# On the road
1. Turn your hotspot on your cell phone on.
2. Connect your USB Garmin to Raspberry pi
3. Boot up the Raspberry pi. 
4. Now you can connect with your cell phone to the your Raspberry pi ( for me it is http://raspberrypi.local. )
5. Use the 'mount' button to mount the USB disk
6. now you can use the upload form to upload gpx file.

7. Use the 'umount' button to umount the USB disk
8. Detach the USB Garmin
9. Refresh the page by clicking the title, and use the 'halt' button to shutdown the Raspberry pi.


