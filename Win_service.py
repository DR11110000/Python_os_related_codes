# Here am giving you all the steps for creating WinService using Python.
''' I faces alot issue due to their is no stepwise procedure for creating the Windows Service using Python, I manage all those things and now 
    i am going to put all those steps in single file.'''
    
#Step 1: Create Win_service.py file.3

import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import psutil

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
                   with open('F:\\ChromeTest.log', 'a') as f:
                       name = process.name()
                       pid = process.pid()
                       f.write("Chrome is running\n")
                       break
                       f.close()
                                 
                   
           rc = win32event.WaitForSingleObject(self.hWaitStop, 10000)

 

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)
        
#Step 2: goto your Python folder->Scripts->run cmd as admin and execute the file pywin32_postinstall using "pywin32_postinstall -install"  eg. F:\Python Installer\Scripts\pywin32_postinstall
#Step 3: goto cmd/powershell and run as adminstrator and then jump to your win_service.py dir and exceute the win_service.py using cmd "python win_service.py install", This will install the service into ur local Machine
#Step 4: open the service.msc and then select your service and double-click and goto Lonon-> change setting to This account. This account will ask u username and password. Enter the username and password then apply the changes. This step eliminates the error like 1053.
#step 5: start service.
