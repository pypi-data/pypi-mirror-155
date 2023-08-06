from typing import Union
from clicknium.common.models.sapitem import SapStatusBarInfo
from clicknium.core.service.invokerservice import _ExceptionHandle, _InvokerService, LocatorService
from clicknium.locator import _Locator

class Sap(object):

    def __init__(self):
        self._sap_driver = _InvokerService.get_sapdriver()

    @_ExceptionHandle.try_except
    def login(
        self,
        login_path: str,
        connection: str,
        client: str,
        user: str,
        password: str,
        timeout: int = 30
    ) -> None:
        """
            Login in sap application.

            Parameters:

                login_path[Required]: login path string, sap application login path

                connection[Required]: connection string, sap application connection

                client[Required]: client string, sap application client

                user[Required]: user string, sap application user

                password[Required]: password string, sap application password

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._sap_driver.Login(login_path, connection, client, user, password, timeout * 1000)

    @_ExceptionHandle.try_except
    def call_transaction(
        self,
        locator: Union[_Locator, str],
        transaction_code: str,
        locator_variables: dict = {},
        timeout: int = 30
    ) -> None:
        """
            Call sap transaction.
 
            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.sap.transaction_input', locator store is sap, locator name is transaction_input

                transaction_code[Required]: transaction code string

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        self._sap_driver.CallTransaction(locator_item.Locator, transaction_code, locator_item.Locator_Variables, timeout * 1000)
        pass

    @_ExceptionHandle.try_except
    def select_item(
        self,
        locator: Union[_Locator, str],
        item: str,
        locator_variables: dict = {},
        timeout: int = 30
    ) -> None:
        """
            Select sap item.
 
            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.sap.item_q', locator store is sap, locator name is item_q

                item[Required]: item string, which is set to be selected

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        self._sap_driver.SelectItem(locator_item.Locator, item, locator_item.Locator_Variables, timeout * 1000)

    @_ExceptionHandle.try_except
    def get_statusbar(
        self, 
        locator: Union[_Locator, str],
        locator_variables: dict = {}, 
        timeout: int = 30
    ) -> SapStatusBarInfo:
        """
            Get sap status bar info.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.sap.satus_bar_q', locator store is sap, locator name is satus_bar_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                SapStatusBarInfo object.
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        statusbar_info = self._sap_driver.ReadStatusBar(locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)
        return SapStatusBarInfo(statusbar_info)


        