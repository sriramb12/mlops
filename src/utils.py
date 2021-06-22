import os
import logging
import sys
import time

'''
function: getProcList
Description: Given a process name or part of a process name, returns all matching processes running
Input: substring of the processname
Output: return the process info (pid, command used to run)
'''
def getProcList(match, exclude = 0):
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    procList = []

    for pid in pids:
        pidfname = '/proc/' + pid + '/cmdline'
        f = open(pidfname)
        cmdline = f.readline()
    
        if not cmdline.startswith(match) :
            continue
        if int(pid) == int(exclude): 
            continue
        procList += [(pid, cmdline)]
    return(procList)

'''
function: setupLogging
Description: sets up logging 
Input: filename
Output: return the logging object
'''
def setupLogging(logfile):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler) 

# create logger
    try:
       logging.basicConfig( level=logging.INFO, 
       format='%(asctime)s [%(levelname)s] - %(message)s', filename= logfile)  # pass explicit filename here 
    except:
       logging.basicConfig( level=logging.INFO, 
       format='%(asctime)s [%(levelname)s] - %(message)s', filename= logfile, mode = 'a+')  # pass explicit filename here 

#    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger = logging.getLogger()

    return logger

'''
function: timeit
Description: Decorator for measuring execution time of a method
Input: method
Output: returns a method 
'''
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

if __name__ == "__main__":
#test code
    match = 'test' 
    print(getProcList(processPrefix))
