from abc import ABC, abstractmethod
from utils import setupLogging
from mldb import MLDB
# NOTE: The ML Model class is abstract and classified into 

class MLApp(ABC):
    @abstractmethod
    def __init__(self, modelName):
        self.name = modelName
        logFile = modelName + '.log'
        self.logging = setupLogging(logFile)
        self.logging.info("initialized Application {0}".format(modelName))
        self.confdb = MLDB(modelName)

    def log(self, logtext):
        self.logging.warn(logtext)
    # at start of model app, build the model (must be overridden in a realworld app
    def buildModel(self, data, target):
       pass 
    #Domain Rules  (Please note : these rules are neither exhaustive nor relevant for all ML models)
    #1.Detect and report Dependency changes
    def checkDependency():
    #Data invariants hold in training and serving inputs, i.e. monitor Training/Serving Skew
        pass

    def checkInvariants():
    #Training and serving features compute the same values
        pass

    def checkTrainingTestFeatures():
    #Models are not too stale
        pass

    def checkModelStale():
    #The model is numerically stable
        pass

    def checkNumericStability():
    #The model has not experienced dramatic or slow-leak regressions in training speed, serving latency, throughput, or RAM usage
        pass

    def checkPerfMetric():
    #The model has not experienced a regression in prediction quality on served data
        pass
    
    def checkRegressionIssues():
        pass

    #Add more checkXXXX() functions as time progresses 
