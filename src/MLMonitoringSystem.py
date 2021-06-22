#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Assumptions:
   * ML applications processes (MLAP) are spawned via this application though run as independent  processes
   * MLMonitoring application process (MLMP) connects to a specific MLAP rest API and issues a command
   * Some python modules are assumed to be installed (till build/packaging is finished)
   * Database installation/setup are already done with necessary users/tables


Central theme of this approach: 
MLMS is the driver (controller) process which 
1) Spawns all MLAP(s) as per the DB/config file
2) Spawns a WEB Server which talks to the clients 
3) Processes Database/information stored by various MLAP processes and generates alerts

Constraints:
1. Only one application instance is run

TODOs
1  Testing using unittest module
2. Implementing Configuration DB. It will take a bit more time. In such case, just the DB connection is
   read from the 'ini' file and the rest are read from DB. Such an approach is more failsafe/robust
3. Not implemented in a distributed manner but can be easily extended to be so.
   In a distributed environment, there are several possibilites 
    a) Distributed MLAPs (supporting a slew of ml algorithms running across several computes
    b) Distributed MLMS (agent/master mode). This will be an extreme case of overcrowded scenario
       
   a) performance
4. Add RESTful interfaces for ML Monitoring System (For dashboard/debugging/troubleshooting)
   which can serve:
       list of MLApps actively running and more details
5. Best practices of Pythonic coding/building to make it production ready and maintainable

6. Continuous improvements in 
   a) coding style
   b) design
   c) performance

'''

import subprocess
import mysql.connector
from threading import Thread
import logging
import json
import redis
import signal
import sys
import os
from time import sleep
from utils import getProcList, setupLogging
from mldb import MLDB



class MLMonitoringSystem:


    def __init__(self, redisServer= '172.17.0.2'):

       self.redisServer = redisServer 
       self.configDb = redis.Redis(host=redisServer, port = 6379)
       assert self.configDb , "Redis not reachable?" + redisServer
       # catch signals such as signal Ctrl + c so we can perform shutdown properly

       for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
            signal.signal(sig, self.shutdown)

       # When ML apps die

       signal.signal(signal.SIGCHLD, self.handleMLAppExit)

    #Handles any crashed out ML App and restarts
    def handleMLAppExit(self, sig, frame):
        self.logger.error('handling ML process exited')
        for model, procList in self.processTable.items():
           self.logger.error('checking {0}'.format(model))
           execFile = procList[0][0]
           args = procList[0][1]
           diedProc = None
           for proc in procList[1:]:
               #print(proc.pid)
               if proc.poll():
                  msg = "The process died for {0}, PID {1}".format(model,proc.pid)
                  mlApp =  MLApp()
                  self.logger.error(msg)
                  diedProc = proc
                  #from process context
                  proc = subprocess.Popen([execFile, args],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
                  procList += [proc]
                  break
        assert(diedProc) 
        procList.remove(diedProc)

    #periodic DB processor for generating any alerts
    def processMLDB(self, arg):
       while True:
          self.logger.debug("processing mldb")
          sleep(15) #TODO : add to conf db

    #run loop
    def foreverLoop(self):
       pass

    #Runs the periodic and any async requests (such as REST commands)
    def run(self):
        #Spawn threads for app monitoring etc
        self.mldbThread = Thread(target = self.processMLDB, args = (10, ))
        self.mldbThread.start()
        self.foreverLoop = Thread(target = self.foreverLoop)
        return

    def initialize(self):
        #logFolder = self.configDb.get('logFolder')
        logFolder = "../run/log"
        try:
            os.makedirs(logFolder)
        except:
            # already exists
            pass
        assert logFolder
        logFile = logFolder + '/mlms.log'
        self.logger = setupLogging(logFile)

       # check if mlms is already running

        myPid = os.getpid()
        isRunning = getProcList('MLMonitoringSystem', myPid)
        if isRunning:
            self.logger.error( 'Monitoring system is already running as process id ' \
                + isRunning[0][0])
            exit(0)
        self.logger.warning( 'Starting monitoring application with pid: ' + str(myPid))
        self.logger.warning( 'Starting monitoring application with pid: ' + str(myPid))

       # connect to DB


    def list(self):
        resp = ''
        # Serializing json   
        jsonList = json.dumps(self.processTable, indent = 4)  
        print(jsonList)
        return jsonList

    def shutdown(self, sig, frame):

      # perform necessary checkpoints
      # terminate self

        self.logger.warning( 'shutting down monitoring application')
        exit(0)


if __name__ == '__main__':
    logFile='../run/log/run.log'
    logger = setupLogging()
    logger.info('Started ML Monitoring Application')
    mlms = MLMonitoringSystem()
    mlms.initialize()
    mlms.run()
    logger.info('started')
