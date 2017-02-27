from ultraSuperbAPI import api

#Take some quality arguments.
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-e", "--environment", help="Choose an environment (DEV, PROD) to run the script as.")

args = parser.parse_args()

#Let the user pick the environment. Defaults to PROD.
if args.environment == "DEV":
    env = "DEV"
elif args.environment == "PROD":
    env = "PROD"
else:
    env = "PROD"


#More quality code here.
####Some Config to externalise.


#Using Python's built in config module.
import configparser
config = configparser.ConfigParser()
#Have a look at the config file.
config.read('ultra.config')

#The Bind IP for the built in flask server.
ServerBindIP = config[env]["server_bind_ip"] #May I suggest you change this if not on a private network?
#Will debig mode be on or off?
DebugMode = bool(config[env]["debug"]) #Running this while I'm devving it up. Maybe will set some command line args at some stage?
#The port to listen on.
ListenPort = int(config[env]["server_port"])

#Some ASCII goodness.
print("""

 _   _ _ _               _____                       _        ___  ______ _____
| | | | | |             /  ___|                     | |      / _ \ | ___ \_   _|
| | | | | |_ _ __ __ _  \ `--. _   _ _ __   ___ _ __| |__   / /_\ \| |_/ / | |
| | | | | __| '__/ _` |  `--. \ | | | '_ \ / _ \ '__| '_ \  |  _  ||  __/  | |
| |_| | | |_| | | (_| | /\__/ / |_| | |_) |  __/ |  | |_) | | | | || |    _| |_
 \___/|_|\__|_|  \__,_| \____/ \__,_| .__/ \___|_|  |_.__/  \_| |_/\_|    \___/
                                    | |
                                    |_|

===============================================================================
===============================================================================

Look, it's a really, really, really bad API!

+-+-+-+-+ +-+-+-+ +-+-+-+-+
|F|e|e|l| |t|h|e| |b|u|r|n|
+-+-+-+-+ +-+-+-+ +-+-+-+-+

The user of this takes responsibility for any compromise that may occur on their
computer.

Written by Reece Payne sometime between 2016 and 2017.

THE FUTURE IS NOW!

""")

api.run(host=ServerBindIP, debug=DebugMode, port=ListenPort)
