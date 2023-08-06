from typing import List, Union
from clicknium.core.models.uielement import UiElement
from clicknium.locator import _Locator
from clicknium.core.service.invokerservice import _ExceptionHandle, _InvokerService


class BrowserTab(object):    

    def __init__(self, tab_object):
        self._tab = tab_object 

    @property
    @_ExceptionHandle.try_except
    def title(self) -> str:
        """
            Get tab's title.
                                
            Returns:
                str
        """
        return self._tab.PageTitle

    @property
    @_ExceptionHandle.try_except
    def url(self) -> str:
        """
            Get tab's url.
                                
            Returns:
                str
        """
        return self._tab.Url

    @property
    @_ExceptionHandle.try_except
    def is_active(self) -> bool:
        """
            Determine if the current tab is active.
                                
            Returns:
                bool
        """
        return self._tab.IsActive

    @property
    @_ExceptionHandle.try_except
    def browser(self):
        """
            Get the browser of the current tab.
                                
            Returns:
                Browser
        """
        from clicknium.core.models.web.browser import Browser
        return Browser(self._tab.Browser)

    @_ExceptionHandle.try_except
    def close(self) -> None:
        """
            Close the current tab.

            Returns:
                None
        """
        self._tab.Close()

    @_ExceptionHandle.try_except
    def refresh(self) -> None:
        """
            Refresh the current tab.

            Returns:
                None
        """
        self._tab.Refresh()

    @_ExceptionHandle.try_except
    def goto(
        self,
        url: str
    ) -> None:
        """
            Go to other website in current tab.
 
            Parameters:

                url[Required]: website string, ex: https://www.bing.com
                                            
            Returns:
                None
        """
        self._tab.Navigate(url)

    @_ExceptionHandle.try_except
    def activate(
        self,
        is_topmost: bool = True
    ) -> None:
        """
            Activate current tab.
 
            Parameters:

                is_topmost: bool, whether to set the windows top most
                                            
            Returns:
                None
        """
        self._tab.Activate(is_topmost)

    def find_element(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {}
    ) -> UiElement:
        """
            In current opened browser, initialize ui element by the given locator.

            Remarks: 
                1.Use "ctrl + f10" to record locator.
                2.It should be used like clicknium.chrome.open("https://bing.com").find_element(), it is different with clicknium.find_element() clicknium.find_element when locating the ui element.
                    clicknium.find_element() is for both web and window's uielement, and does not specified a scope to locate the element
                    clicknium.chrome.open("https://bing.com").find_element() will locate element in the specified browser
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator
 
            Returns:
                UiElement object, you can use the uielement to do the following operation, such as click, set_text, before operating, it will try locate the element to verify whether the element exist
        """
        ele = _InvokerService.find_element_web(self._tab, locator, locator_variables)
        return UiElement(ele)

    def find_elements(
        self,
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
        results = _InvokerService.find_elements_web(self._tab, locator, locator_variables, timeout)
        if results:
            for element in results:
                elements.append(UiElement(element))
        return elements

    def wait_disappear(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> bool:
        """
            In current opened browser, wait for the element disappear.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                wait_timeout: wait timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                bool, return True if the element is disappear in given time or return False
        """ 
        result = _InvokerService.wait_disappear_web(self._tab, locator, locator_variables, wait_timeout)
        return True if result else False

    def wait_appear(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> UiElement:
        """
            In current opened browser, wait for the element appear.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                wait_timeout: wait timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                UiElement object, or None if the element is not appear
        """ 
        ele = _InvokerService.wait_appear_web(self._tab, locator, locator_variables, wait_timeout)
        if ele:
            return UiElement(ele)
        return None

    def is_exist(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        timeout: int = 30
    ) -> bool: 
        """
            In current opened browser, check whether the ui element exist or not.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                return True if ui element exist, or return False
        """    
        result = _InvokerService.is_exist_web(self._tab, locator, locator_variables, timeout)
        return True if result else False

    def wait_property(
        self,
        locator: Union[_Locator, str],
        name: str,
        value: str,
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> bool:
        """
            Wait web element's property appears in given time with attaching browser.
 
            Parameters:
                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                name[Required]: property name, different ui elements may support different property list, for general property list, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/property

                value[Required]: expected property value

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                wait_timeout: wait timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                bool, return True if ui element exist and the property value equals expected value, or return False
        """   
        result = _InvokerService.wait_property_web(self._tab, locator, name, value, locator_variables, wait_timeout)
        return True if result else False

    def set_property(
        self,
        locator: Union[_Locator, str],
        name: str,
        value: str,
        locator_variables: dict = {},
        timeout: int = 30
    ) -> None:
        """
            Set web element's property value.
 
            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                name[Required]: property name, different ui elements may support different property list, for general property list, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/property

                value[Required]: property value

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        _InvokerService.set_property_web(self._tab, locator, name, value, locator_variables, timeout)

    def execute_js(
        self,
        locator: Union[_Locator, str], 
        javascript_code: str, 
        method_invoke: str = '', 
        locator_variables: dict = {}, 
        timeout: int = 30
    ) -> str:
        """
            Execute javascript code snippet for the target element.

            Remarks: 
                1.For javascript code, use "_context$.currentElement." as the target element. 

                2.For method invoke, valid method_invoke string should like "run()", or when passing parameters should like "run("execute js", 20)".
 
            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                javascript_code[Required]: javascript code snippet string, execute code to target element, use "_context$.currentElement." as the target element, ex: "function SetText(st){_context$.currentElement.value = st; console.log("execute js"); return \"success\"}"

                method_invoke: method invoker string, should like "run()", or when passing parameters should like "run("execute js", 20)", ex: for above javascript code, we can set to "SetText(\"execute\")"

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                str
        """
        return _InvokerService.execute_js(self._tab, locator, javascript_code, method_invoke, locator_variables, timeout)

    def execute_js_file(
        self,
        locator: Union[_Locator, str], 
        javascript_file: str, 
        method_invoke: str = '', 
        locator_variables: dict = {}, 
        timeout: int = 30
    ) -> str:
        """
            Execute javascript file for the target element.

            Remarks: 
                1.For javascript script, use "_context$.currentElement." as the target element. 

                2.For method invoke, valid method_invoke string should like "run()", or when passing parameters should like "run("execute js", 20)".
 
            Parameters:

                locator[Required]: locator string, the name of one locator in locator store, ex: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, locator name is search_sb_form_q

                javascript_file[Required]: javascript file, execute code to target element, use "_context$.currentElement." as the target element, ex: we can set javascript file's content as "function SetText(st){_context$.currentElement.value = st; console.log("execute js"); return \"success\"}"

                method_invoke: method invoker string, should like "run()", or when passing parameters should like "run("execute js", 20)", ex: for above javascript code, we can set to "SetText(\"execute\")"

                locator_variables: locator variables, is set to initialize parameters in locator, ex: var_dict = { "row": 1, "column": 1}, more about variable, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/parametric_locator

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                str
        """
        with open(javascript_file, "r") as f:
            javascript_code = f.read()
        return _InvokerService.execute_js(self._tab, locator, javascript_code, method_invoke, locator_variables, timeout)