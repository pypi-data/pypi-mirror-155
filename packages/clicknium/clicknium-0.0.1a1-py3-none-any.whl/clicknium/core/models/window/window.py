from typing import Union
from clicknium.core.service.invokerservice import _ExceptionHandle, _InvokerService, LocatorService
from clicknium.locator import _Locator

class Window(object):

    def __init__(self):
        self._window_driver = _InvokerService.get_windowdriver()

    @_ExceptionHandle.try_except
    def maximize(
        self, 
        locator: Union[_Locator, str],
        locator_variables: dict = {}, 
        timeout: int = 30
    ) -> None:
        """
            Maximize the window.

            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.notepad.window_notitle_notepad', locator store is notepad, locator name is window_notitle_notepad

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        self._window_driver.SetMaximize(locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)

    @_ExceptionHandle.try_except
    def minimize(
        self, 
        locator: Union[_Locator, str],
        locator_variables: dict = {}, 
        timeout: int = 30
    ) -> None:
        """
            Minimize the window.

            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.notepad.window_notitle_notepad', locator store is notepad, locator name is window_notitle_notepad

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        self._window_driver.SetMinimize(locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)

    @_ExceptionHandle.try_except
    def restore(
        self, 
        locator: Union[_Locator, str],
        locator_variables: dict = {}, 
        timeout: int = 30
    ) -> None:
        """
            Restore the window.

            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.notepad.window_notitle_notepad', locator store is notepad, locator name is window_notitle_notepad

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        self._window_driver.Restore(locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)