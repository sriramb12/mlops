from mldb import MLDB
import subprocess
from utils import setupLogging
import redis
import signal
from threading import Thread
import json
import time
'''
The models we build should not be monolithic but should be broken so that various steps/phases should be in 
Ops control. Ex the lifeycle of an ML application can comprise of: 
--Data Cleanup
--Data Visualization
--Train Test split
--Build model
--Evaluate accuracy
--Deploy
The above steps should be callable from application interface. If not all, at least, we need to be able to call
Build, Evaluate and deploy using API (class methods)
the following code makes such assumption(s)

Based on careful considerations of such aspects, we can make some code refactoring to super (MLModelApp) class

'''
   
class AppManager():
    def __init__(self, redisServer, redisPort = 6379):
        logFolder = "../run/log"
        self.logFile = logFolder + '/appManager.log'
        self.logger = setupLogging(self.logFile)
        self.redisServer = redisServer
        self.configDb = redis.Redis(host = redisServer, port = redisPort)
        assert self.configDb , "Redis not reachable?" + redisServer
        signal.signal(signal.SIGCHLD, self.handleMLAppInstExit)
        pass

    #Handles any crashed out ML App and restarts
    def handleMLAppInstExit(self, sig, frame):
        self.logger.error('handling ML process exited')
        deadProc = None
        for model, procList in self.processTable.items():
           self.logger.info('checking {0}'.format(model))
           execFile = procList[0][0]
           args = procList[0][1]
           for proc in procList[1:]:
               if proc.poll():
                  msg = "The process died for {0}, PID {1}".format(model,proc.pid)
                  self.logger.error(msg)
                  deadProc = proc
                  break
                  #from process context
           if deadProc:
                   procList.remove(deadProc)
                   proc = subprocess.Popen([execFile, args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                   self.processTable[model] += [proc]
                   self.logger.error('removed proc {0} added proc {1}'.format(deadProc.pid, proc.pid))
                   deadProc = None
                   break
        else:
          self.logger.error("failed to find process in the list") 

    def appMgrDbAlertLoop(self):
        self.logger.debug("looping for alerts") 
        dbAlertFreq = 10
        while True:
          self.logger.info("looping for alerts") 
          time.sleep(dbAlertFreq)
         
        
    def processAppConf(self, appConfFile = '../run/app/app.cfg'):
         with open(appConfFile) as f:
            self.appConf = json.load(f)
            self.logger.info('Spawning ml apps from ' + appConfFile)
            self.processTable = {}
          
            #print(self.appConf)
            for (model, params) in self.appConf.items():
                appLoc = '../run/app/bin/'

                execFile = appLoc + params['binfile']
                args = params['args']
                count = params['instances']
                for i in range(count):
                    mlApp = MLApp(model, execFile, args, self.logger)
                    self.logger.info('Running {0} {1}'.format(execFile, args))
                    proc = subprocess.Popen([execFile, args],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
                    self.logger.info('pid {0}'.format(proc.pid)) 
                    try:
                        self.processTable[model] += [proc]
                    except:
                        self.processTable[model] = [(mlApp, execFile, args)]
                        self.processTable[model] += [proc]
          

class MLApp:
     def __init__(self, model, exe, args, logger):
         logFolder = "../run/log/"
         self.logFile = logFolder + model + '.log'
         self.logger = logger 
         self.logger.info("initialized app {0} bin {1} with args {2}".format(model, exe, args))
         self.model = model
         self.exe = exe
         self.args = args
         pass

     def build(self):
         pass

     def eval(self):
         #return the model performance (confusion matrix or such)
         return 

     def predict(self, featureVector): 
        return predict (featureVector) 

     def run(self):
         self.build()

     def checkPerfMetric(self):
        '''
        Assuming new training data is continuously added, we need to schedule this check
        periodically (say, every 2 weeks or month)
        (model drift?)
        the result will be stored in DB
        '''
        return

     def performChecks(self):
            #run checks
            #self.checkPerfMetric()
            #call the other methods
            pass

     def checkDependency(self):
     #Data invariants hold in training and serving inputs, i.e. monitor Training/Serving Skew
        pass

     def checkInvariants(self):
     #Training and serving features compute the same values
        pass

     def checkTrainingTestFeatures(self):
     #Models are not too stale
        pass

     def checkModelStale(self):
     #The model is numerically stable
        pass

     def checkNumericStability(self):
     #The model has not experienced dramatic or slow-leak regressions in training speed, serving latency, throughput, or RAM usage
        pass

     def checkPerfMetric(self):
     #The model has not experienced a regression in prediction quality on served data
        pass
    
     def checkRegressionIssues(self):
        pass

     def runAppLoop(self):
        self.build() #No op for now

if __name__ == '__main__':
    #mlAppMgr = AppManager(redisServer= '172.17.0.2')
    mlAppMgr = AppManager(redisServer= '127.0.0.1')
    mlAppMgr.processAppConf()
    mlAppMgr.appMgrDbAlertLoop()
