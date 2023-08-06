from clicknium.common.models.sapitem import SapStatusBarInfo
from clicknium.core.service.invokerservice import _ExceptionHandle

class SapElement(object):

    def __init__(self, element):
        self._element = element

    @_ExceptionHandle.try_except
    def call_transaction(
        self,
        transaction_code: str,
        timeout: int = 30
    ) -> None:
        """
            Call sap transaction.
 
            Parameters:

                transaction_code[Required]: transaction code string

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._element.CallTransaction(transaction_code, timeout * 1000)        

    @_ExceptionHandle.try_except
    def select_item(
        self,
        item: str,
        timeout: int = 30
    ) -> None:
        """
            Select sap item.
 
            Parameters:

                item[Required]: item string, which is set to be selected

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._element.SelectItem(item, timeout * 1000)

    @_ExceptionHandle.try_except
    def get_statusbar(
        self, 
        timeout: int = 30
    ) -> SapStatusBarInfo:
        """
            Get sap status bar info.
 
            Parameters:
                timeout: timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                SapStatusBarInfo object.
        """
        statusbar_info = self._element.ReadStatusBar(timeout * 1000)
        return SapStatusBarInfo(statusbar_info)