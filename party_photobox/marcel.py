from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

#kill already running Gphoto2 when turning on/off camera

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'],stdout=subprocess.PIPE)
    out, err = p.communicate()

    #search process line to be killer
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID="WeddingShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100EOS5D", \
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location ="/home/pi/Desktop/Photobooth/images/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print ("Failed to create the new directory. Already existing")
        os.chdir(save_location)

def captureImages():
    gp (triggerCommand)
    gp (downloadCommand)
    gp (clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith("JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith (".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print("Renamed the RAW")

killgphoto2Process()
gp(clearCommand)
createSaveFolder()
captureImages()
renameFiles(picID)
