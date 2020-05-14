import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import psutil
from datetime import datetime

import time
import os


class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TestService"
    _svc_display_name_ = "Test Service"
    _svc_description_ = "My service description"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
           for process in psutil.process_iter():
               if 'chrome' in process.name().lower():
                   with process.oneshot():
                       pid = process.pid
                       name = process.name()
                       time = datetime.fromtimestamp(process.create_time())
                   with open('F:\\ChromeTest.log', 'a') as f:
                      
                       f.write("pid:{} name:{} time:{}".format(pid, name, time))
                       f.close()
                                 
                   
           rc = win32event.WaitForSingleObject(self.hWaitStop, 10000)

 

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)
