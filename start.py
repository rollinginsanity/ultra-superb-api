from ultraSuperbAPI import api
#More quality code here.
####Some Config to externalise.

ServerBindIP = "0.0.0.0" #May I suggest you change this if not on a private network?
DebugMode = True #Running this while I'm devving it up. Maybe will set some command line args at some stage?
ListenPort = 5000 #Literally the flask default.

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
