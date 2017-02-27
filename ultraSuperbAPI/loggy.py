import logging
import os
#Lets break logging.
class crappyLog:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('logs/api.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    #Never, ever, ever, ever let user input select which file to read.
    def view_logs(logfile):
        #Also, be careful when dumping out to shell. CODE EXEC IS HERE TO STAY!
        logs = os.popen("tail logs/"+logfile).read()
        #And now we're also sending back responses from commands run, so it's not blind.
        return logs
