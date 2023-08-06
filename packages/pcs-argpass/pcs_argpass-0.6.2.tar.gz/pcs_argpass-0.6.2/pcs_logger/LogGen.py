#!/usr/bin/env python3
# vim: expandtab:ts=4:sw=4:noai

import logging
import logging.config
import logs
import time
import os
import sys


def SetupLogging(AppName, Verbose = 0, NoDaemon = True, StdErr = False, LogFile = '', Quiet = False, ProcInfo = False):
    logs.add_trace_level()
    logs.add_logging_level('MSG', logging.WARNING - 1, 'msg')
    logs.add_logging_level('STATUS', logging.ERROR - 1, 'status')
    if not NoDaemon:  # Ausgabe auf StdErr macht als Daemon keinen Sinn
        StdErr = False

    if Quiet:  # Wenn Quiet angegeben ist macht Verbose keinen Sinn
        Verbose = -1

    ShowLevel = ' - %(levelno)02d'
    if Verbose == 0:  # Default
        ShowLevel = ''
        LogLevel = logging.MSG
    elif Verbose == 1:  # Mit Messages
        LogLevel = logging.INFO
    elif Verbose == 2:  # Mit debug infos
        LogLevel = logging.DEBUG
    elif Verbose >= 3:  # Mit itrace infos
        LogLevel = logging.TRACE
    else:  # Quiet
        LogLevel = logging.ERROR

    AddPar = ':%(processName)s:%(threadName)s\t' if ProcInfo else ''
    
    if LogFile != '':
        FileLogHand = logging.handlers.TimedRotatingFileHandler(LogFile, when = 'S',interval = 60*60*24, backupCount = 5)
        logging.basicConfig(handlers = [FileLogHand], level = LogLevel, format = f"%(asctime)s - {AppName}{AddPar}{ShowLevel} - %(message)s")
        FileLogHand.doRollover()
    elif StdErr:
        logging.basicConfig(stream = sys.stderr, level = LogLevel, format = f"%(asctime)s {AddPar[1:]}{ShowLevel} - %(message)s")
    else:
        SysLogHand = logging.handlers.SysLogHandler(address = '/dev/log')
        logging.basicConfig(handlers = [SysLogHand], level = LogLevel, format = f"{AppName}{AddPar}{ShowLevel} - %(message)s")




if __name__ == '__main__':
    MyParam= {}
    MyParam['Verbose'] = 3
    MyParam['StdErr'] = True
    MyParam['NoDaemon'] = True
    MyParam['Quiet'] = False
    MyParam['LogFile'] = ''
    MyParam['ProcInfo'] = False

#    MyParam['LogFile'] = './TheLog.log'
    AppName = "LogGen"

    SetupLogging(AppName, 
        Verbose = MyParam['Verbose'], 
        StdErr = MyParam['StdErr'], 
        NoDaemon = MyParam['NoDaemon'], 
        Quiet = MyParam['Quiet'],
        LogFile = MyParam['LogFile'],
        ProcInfo = MyParam['ProcInfo']) 

    logging.error('Error')
    logging.warning('Warning')
    logging.info('Info')
    logging.msg('Msg')
    logging.status('Status')
    logging.trace('Trace')
    logging.debug('Debug')
    logging.status('Start program')
    for i in range(1):
        logging.trace(f'------------{i}')
        logging.warning('Parameters:')
        for key, value in MyParam.items():
            logging.msg(f'  {key} = {value}')
#        time.sleep(5)
