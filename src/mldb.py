from abc import ABC, abstractmethod
from utils import setupLogging
import redis
'''
The mldb will have methods for a specific DB (currently just Redis)
Redis will be used to store configuration and Redis db will be present in any case
'''
class MLDB(ABC):
    def __init__(self, modelName):
        configDb = redis.Redis(host='localhost', port = 6379)

        if not configDb:
           self.logging.warn('no redis server running?')
           exit(0) 
        db = configDb.get('database')
        logFolder = configDb.get('logFolder')
        
        if not db: 
           log = "mldb: initialized database as redis {0}".format(modelName)
           configDb.set('database', 'redis')
           logFolder = '../run/log/'
           configDb.set('rootFolder', '../')
           configDb.set('logFolder', '../log/')
           
        else:
           log = "mldb: found database as {0}".format(db)
        if not logFolder:
           configDb.set('logFolder', '../log/')
           logFolder =  '../log/'
        logFile = logFolder + modelName + '.log'
        self.logger = setupLogging(logFile)
        self.logger.info(log)
        '''
        Based on db parameters, call appropriate db
        '''

    def get(self):
        pass

    def set(self):
        pass 
