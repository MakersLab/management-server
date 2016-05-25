import os
from time import localtime, strftime
pilist = ["0","1","2"]
foldlist = ["rebelix","satoshi","slush"]
cas= strftime("%Y_%m_%d_%H_%M", localtime())
os.system("mkdir "+ cas)
for pi in pilist:
	os.system("mkdir "+cas+"/"+foldlist[int(pi)])
	os.system("mkdir "+cas+"/"+foldlist[int(pi)]+"/home")
	os.system("mkdir "+cas+"/"+foldlist[int(pi)]+"/home/pi")
	os.system("mkdir "+cas+"/"+foldlist[int(pi)]+"/home/pi/.octoprint")
	os.system("mkdir "+cas+"/"+foldlist[int(pi)]+"/home/pi/.octoprint/data")
	os.system("mkdir "+cas+"/"+foldlist[int(pi)]+"/home/pi/.octoprint/data/printhistory")
	print "directories created"
        print "saving user files"
	os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@192.168.2.1"+pi+":/home/pi/.octoprint/users.yaml /home/pi/backupML/"+foldlist[int(pi)]+"/home/pi/.octoprint/users.yaml")
	print "saving printhistory data"
	os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@192.168.2.1"+pi+":/home/pi/.octoprint/data/printhistory/history.yaml "+foldlist[int(pi)]+"/home/pi/.octoprint/data/printhistory/history.yaml")
	print "saving timelapses"
	os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@192.168.2.1"+pi+":/home/pi/.octoprint/timelapse "+foldlist[int(pi)]+"/home/pi/.octoprint/")
	print "saving gcodes"
	os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@192.168.2.1"+pi+":/home/pi/.octoprint/uploads "+foldlist[int(pi)]+"/home/pi/.octoprint/")
	print "saved: "+ foldlist[int(pi)]
print "Backup done!"
