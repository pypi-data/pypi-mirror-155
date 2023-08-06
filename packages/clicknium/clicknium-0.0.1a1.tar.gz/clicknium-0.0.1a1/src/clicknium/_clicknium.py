import sys
from typing import List, Union
from clicknium.common.enums import WindowMode, BrowserType
from clicknium.core.models.window.window import Window
from clicknium.core.models.java.java import Java
from clicknium.core.models.sap.sap import Sap
from clicknium.core.models.uielement import UiElement
from clicknium.core.models.web.basewebdriver import BaseWebDriver
from clicknium.core.models.web.webdriver import WebDriver
from clicknium.core.service.invokerservice import _InvokerService
from clicknium.locator import _Locator

if sys.version_info >= (3, 8):
    from typing import Literal
else: 
    from typing_extensions import Literal

class _Clicknium():

    ie = BaseWebDriver(BrowserType.IE)
    chrome = WebDriver(BrowserType.Chrome)
    firefox = WebDriver(BrowserType.FireFox)
    edge = WebDriver(BrowserType.Edge)
    window = Window()
    sap = Sap()
    java = Java()    

    @staticmethod
    def find_element(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        window_mode: Literal["auto", "topmost", "noaction"] = WindowMode.Auto
    ) -> UiElement:

        """
            Initialize ui element by the given locator.

            Remarks: 

                1.Use "ctrl + f10" to record locator.

                2.Import parameter module with " from clicknium.common.enums import * "
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                window_mode: Window mode define whether to set the window on topmost for the following operation on the element  

                    Auto: Default value is auto, it means setting the window automatically, we set the internal context for automation operation, the context stores info about the ui element operated just now, include process name, main window title etc. if current ui element's info is same as previous, then don't need set window topmost as it should be already set; or will set window topmost  
                    TopMost: always setting the window on topmost  
                    NoAction: always don't setting the window on topmost  
 
            Returns:
                UiElement object, you can use the uielement to do the following operation, such as click, set_text, before operating, it will try locate the element to verify whether the element exist
        """
        ele = _InvokerService.find_element(locator, locator_variables, window_mode)
        return UiElement(ele)

    @staticmethod
    def find_elements(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        timeout: int = 30
    ) -> List[UiElement]:

        """
            Find elements by the given locator.

            Remarks: 

                1.Use "ctrl + f10" to record locator.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                list of UiElement object, you can use each of the uielement to do the following operation, such as click, set_text, before operating, it will try locate the element to verify whether the element exist
        """
        elements = []
        results = _InvokerService.find_elements(locator, locator_variables, timeout)
        if results:
            for element in results:
                elements.append(UiElement(element))
        return elements

    ui = find_element

    @staticmethod
    def send_hotkey(hotkey: str) -> None:
        """
            Send hotkey to current cursor's position.
 
            Parameters:
                hotkey: hotkey string, can be one key or combined keys, each key is represented by one or more characters. To specify a single keyboard character, use the character itself. For example, to represent the letter A, pass in the string "A" to the method. To represent more than one character, append each additional character to the one preceding it. To represent the letters A, B, and C, specify the parameter as "ABC". For special keys, please refer to https://docs.microsoft.com/en-au/dotnet/api/system.windows.forms.sendkeys?view=windowsdesktop-6.0#remarks
                                
            Returns:
                None
        """
        _InvokerService.send_hotkey(hotkey)

    @staticmethod
    def send_text(text: str) -> None:
        """
            Send text to current cursor's position.
 
            Parameters:

                text[Requried]: text string, is sent to be input

            Returns:
                None
        """
        _InvokerService.send_text(text)

    @staticmethod
    def wait_disappear(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> bool:
        """
            Wait element disappears in given time.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                wait_timeout: wait timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                bool, return True if the element is disappear or return False
        """ 
        result = _InvokerService.wait_disappear(locator, locator_variables, wait_timeout)
        return True if result else False

    @staticmethod
    def wait_appear(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> UiElement:
        """
            Wait element appears in given time.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                wait_timeout: wait timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                UiElement object, or None if the element is not appear
        """      
        ele = _InvokerService.wait_appear(locator, locator_variables, wait_timeout)
        if ele:
            return UiElement(ele)
        return None

    @staticmethod
    def is_exist(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        timeout: int = 30
    ) -> bool:
        """
            Determine if an element exists.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                return True if ui element exist, or return False
        """        
        result = _InvokerService.is_exist(locator, locator_variables, timeout)
        return True if result else False

    @staticmethod
    def wait_property(
        locator: Union[_Locator, str],
        name: str, 
        value: str, 
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> bool:
        """
            Wait element's property appears in given time.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                name[Required]: property name, different ui elements may support different property list, for general property list, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/property

                value[Required]: expected property value

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                wait_timeout: wait timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                bool, return True if ui element exist and the property value equals expected value, or return False
        """        
        result = _InvokerService.wait_property(locator, name, value, locator_variables, wait_timeout)
        return True if result else False
