from clicknium.core.models.uielement import UiElement
from clicknium.core.service.invokerservice import _ExceptionHandle

class WebElement(UiElement):

    def __init__(self, element):
        super(WebElement, self).__init__(element)

    @property
    @_ExceptionHandle.try_except
    def parent(self):
        """
            Get parent element.
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        if self._element.Parent:
            return WebElement(self._element.Parent)
        return None

    @property
    @_ExceptionHandle.try_except
    def children(self):
        """
            Get element's children elements.
                                
            Returns:
                list of WebElement object, a list with elements if any was found or an empty list if not
        """
        child_list = []
        if self._element.Children:            
            for child in self._element.Children:
                child_list.append(WebElement(child))
        return child_list

    @property
    @_ExceptionHandle.try_except
    def next_sibling(self):
        """
            Get next sibling element.
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        if self._element.NextSibling:
            return WebElement(self._element.NextSibling)
        return None

    @property
    @_ExceptionHandle.try_except
    def previous_sibling(self):
        """
            Get previous sibling element.
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        if self._element.PreviousSibling:
            return WebElement(self._element.PreviousSibling)
        return None
    
    @_ExceptionHandle.try_except
    def child(self, index: int):
        """
            Get child element with its index.

            Parameters:
                index: index specified, get the nth child
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        child_element = self._element.Child(index)
        if child_element:
            return WebElement(self._element.Child(index))
        return None

    @_ExceptionHandle.try_except
    def set_property(
        self,
        name: str,
        value: str,
        timeout: int = 30
    ) -> None:
        """
            Set web element's property value.
 
            Parameters:

                name[Required]: property name, different ui elements may support different property list, for general property list, please refer to https://clicknium.github.io/product-docs/#/./doc/automation/property

                value[Required]: property value

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._element.SetProperty(name, value, timeout * 1000)

    @_ExceptionHandle.try_except
    def execute_js(
        self,
        javascript_code: str, 
        method_invoke: str = '', 
        timeout: int = 30
    ) -> str:
        """
            Execute javascript code snippet for the target element.

            Remarks: 
                1.For javascript code, use "_context$.currentElement." as the target element. 

                2.For method invoke, valid method_invoke string should like "run()", or when passing parameters should like "run("execute js", 20)".
 
            Parameters:

                javascript_code[Required]: javascript code snippet string, execute code to target element, use "_context$.currentElement." as the target element, ex: "function SetText(st){_context$.currentElement.value = st; console.log("execute js"); return \"success\"}"

                method_invoke: method invoker string, should like "run()", or when passing parameters should like "run("execute js", 20)", ex: for above javascript code, we can set to "SetText(\"execute\")"

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                str
        """
        return self._element.ExecuteJavaScript(javascript_code, method_invoke, timeout * 1000)

    @_ExceptionHandle.try_except
    def execute_js_file(
        self,
        javascript_file: str, 
        method_invoke: str = '', 
        timeout: int = 30
    ) -> str:
        """
            Execute javascript file for the target element.

            Remarks: 
                1.For javascript script, use "_context$.currentElement." as the target element. 

                2.For method invoke, valid method_invoke string should like "run()", or when passing parameters should like "run("execute js", 20)".
 
            Parameters:

                javascript_file[Required]: javascript file, execute code to target element, use "_context$.currentElement." as the target element, ex: we can set javascript file's content as "function SetText(st){_context$.currentElement.value = st; console.log("execute js"); return \"success\"}"

                method_invoke: method invoker string, should like "run()", or when passing parameters should like "run("execute js", 20)", ex: for above javascript code, we can set to "SetText(\"execute\")"

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                str
        """
        with open(javascript_file, "r") as f:
            javascript_code = f.read()
        return self._element.ExecuteJavaScript(javascript_code, method_invoke, timeout * 1000)
