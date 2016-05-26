
def backup():
    import os
    from time import localtime, strftime
    from modules.generateNames import generateNames
    try:
        list= generateNames('printers.txt')
        time = strftime("%Y_%m_%d_%H_%M", localtime())
        os.system("mkdir " + time)
        for item in list:
            os.system("mkdir " + time + "/" + item['name'])
            os.system("mkdir " + time + "/" + item['name'] + "/home")
            os.system("mkdir " + time + "/" + item['name'] + "/home/pi")
            os.system("mkdir " + time + "/" + item['name'] + "/home/pi/.octoprint")
            os.system("mkdir " + time + "/" + item['name'] + "/home/pi/.octoprint/data")
            os.system("mkdir " + time + "/" + item['name'] + "/home/pi/.octoprint/data/printhistory")
            print("directories created")
            print("saving user files")
            os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@" + item['address'] + ":/home/pi/.octoprint/users.yaml /home/pi/backupML/" + item['name'] + "/home/pi/.octoprint/users.yaml")
            print("saving printhistory data")
            os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@" + item['address']+ ":/home/pi/.octoprint/data/printhistory/history.yaml " + item['name'] + "/home/pi/.octoprint/data/printhistory/history.yaml")
            print("saving timelapses")
            os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@" + item['address'] + ":/home/pi/.octoprint/timelapse " + item['name'] + "/home/pi/.octoprint/")
            print("saving gcodes")
            os.system("rsync -e 'ssh -i /home/pi/.ssh/id_rsa' -avzp pi@" + item['address'] + ":/home/pi/.octoprint/uploads " + item['name'] + "/home/pi/.octoprint/")
            print("saved: " + item['name'])
            print("Backup done!")
        return True,''
    except Exception as e:
        return False,str(e)