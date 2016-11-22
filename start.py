from ultraSuperbAPI import api

####Some Config to externalise.

ServerBindIP = "0.0.0.0" #May I suggest you change this if not on a private network?
DebugMode = True #Running this while I'm devving it up. Maybe will set some command line args at some stage?
ListenPort = 5000 #Literally the flask default.

api.run(host=ServerBindIP, debug=DebugMode, port=ListenPort)
