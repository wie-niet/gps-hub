#!/usr/bin/env python 
import os

from flask import Flask, request, redirect, url_for, jsonify, render_template, render_template_string
from werkzeug import secure_filename
import sh
import random

import GarminGpsMassStorage

gps = GarminGpsMassStorage.GarminGpsMassStorage(mount_point='/mnt/GPS',dev_path="/dev/disk/by-label/GARMIN")
# let's abuse the gps object as data container to hold our special halt_secret
gps.halt_secret = None

app = Flask(__name__)

#
# our main page
#
@app.route("/")
def index():
    return render_template('index.html', gps=gps, folderNames=['UserDataSync', 'GeotaggedPhotos'])

#
# actions mount/umout/halt/file upload etc.
#
@app.route("/action", methods=['POST'])
def pageAction():
    # action nothing: redirect back to index
    if request.form['action'] == "nothing":
        return redirect(url_for('index'))

    # action mount usb disk
    if request.form['action'] == "mount":
       gps.mount()
        
    # action read GarminDevice.xml config file
    elif request.form['action'] == "read_device_xml":
       gps.readGarminDeviceXml()

    # action umount usb disk (a.k.a. eject )
    elif request.form['action'] == "umount":
       gps.umount()

    # action bring system to a proper halt
    elif request.form['action'] == "system_halt":
       if gps.isMounted() is False:
           if gps.isDevExists() is False:
       	       # let's add an extra step 
               if gps.halt_secret == int(request.form['halt_secret']):
       	           sh.halt()
       	           return """ system going for halt """
       	       else:
                   # generate a temporary halt_secret 
                   gps.halt_secret = random.randint(0,10e10)
                   return render_template('halt.html', halt_secret=gps.halt_secret)

       	   else:
       	       return """ gps is still conected """
       else:
           return """ gps is still mounted """


    # action upload file 
    elif request.form['action'] == "file_upload":
       folderName = request.form['folder_name']
       uploadPath = gps.getFolderPathByName(folderName)
       extension = gps.getFolderExtensionByName(folderName)

       file = request.files['file']
       if file and file.filename.lower().endswith('.'+extension.lower()):
           filename = secure_filename(file.filename)
           file.save(os.path.join(uploadPath, filename))
       else:
           return """error: no valid file ..."""
	
    # action invalid
    else:
       return """error: no valid action given..."""

    return redirect(url_for('index'))



#
# run the server
#
app.run(host='0.0.0.0', port=80, debug=True)

