import os
from clicknium.common.constants import _Constants
from clicknium.common.enums import BrowserType
from clicknium.common.models.exceptions import ExtensionOperationError
from clicknium.common.utils import Utils


class WebExtension(object):

    def __init__(self, browser_type):        
        if browser_type == BrowserType.Chrome:
            self.browser_identity = "Chrome" 
        elif browser_type == BrowserType.FireFox:
            self.browser_identity = "FireFox" 
        elif browser_type == BrowserType.Edge:
            self.browser_identity = "Edge" 
        else:
            self.browser_identity = None
        lib_folder = Utils.get_automation_libfolder()
        self.exe_path = os.path.join(lib_folder, "Clicknium.Web.ExtensionInstaller.exe")

    def install(self) -> None: 
        """
            Install web extension.

            Remarks:  

                1.Before installing extension, you should make sure you have already closed edge, firefox and chrome browser.

                2.When extension is installed successfully, then you should turn on the extension manually.
                                            
            Returns:
                None
        """            
        if self.browser_identity:
            print(_Constants.ExtensionOperationStart % ("install", self.browser_identity))
            cmd = "cmd/c %s -install -t %s -l en-US" % (self.exe_path, self.browser_identity)
            result = os.system(cmd)
            if result:
                error = Utils.resolveWebExtensionExitCode(result, self.browser_identity, "installation")
                print(error)
                raise ExtensionOperationError("Install", self.browser_identity, error)
            else:
                print(_Constants.BrowserOperationEnd % ("Install", self.browser_identity, self.browser_identity))            

    def update(self) -> None:
        """
            Update web extension.
                                        
            Returns:
                None
        """ 
        if self.browser_identity:
            print(_Constants.ExtensionOperationStart % ("update", self.browser_identity))
            cmd = "cmd/c %s -update -t %s -l en-US" % (self.exe_path, self.browser_identity)
            result = os.system(cmd)
            if result:
                error = Utils.resolveWebExtensionExitCode(result, self.browser_identity, "update")
                print(error)
                raise ExtensionOperationError("Update", self.browser_identity, error)
            else:
                print(_Constants.BrowserOperationEnd % ("Update", self.browser_identity, self.browser_identity))    