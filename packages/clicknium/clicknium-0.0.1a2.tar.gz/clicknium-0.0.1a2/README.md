# Clicknium python SDK
Clicknium python sdk provides methods to automate various applications, such as Web browser, Windows Desktop application, Java application, Sap windows Gui app, etc. You can get official API document from [here](https://www.clickcorp.com/documents).

# Getting started
Clicknium is powered by [ClickCorp](https://www.clickcorp.com), besides python sdk, we also provide extension for Visual Studio Code to help you record the UI element and write python code easily.

## Clicknium extension for Visual Studio Code

This extension helps you capture and manage UI locators easily. Unlike selenium or playwright that you need to figure out the locator by XPath or CssSelector. Clicknium extension generates locator by just clicking the target UI element, with [clicknium python module](https://pypi.org/project/clicknium/), you can start automation for web and desktop right away. Besides generating locators automatically, it also provides locator intellisense in coding, centralized locator management in cloud, and project for distribution.

# Installation
## System Requirement
- Python 3.7 or above
- Windows 7 SP1 or above

## Install Clicknium Visual Studio Code extension
Click the following link to install [Clicknium Visual Studio Code extension](),
After installation, you need sign in to ClickCorp  
![login](https://clickcorp.github.io/clicknium-docs/doc/img/login1.png "login")   
Click 'Allow' to open ClickCorp website to sign up and sign in, we support 'Sign in with Google and GitHub' too.

## Install Clicknium python module
Install Clicknium automation sdk through [pip](https://pypi.org/project/clicknium/)  

```
# python version is 3.8 or below
pip install clicknium

# python version is 3.9 or above
pip install --pre pythonnet
pip install clicknium
```

# Create project
- Install browser extension
  Click 'Clicknium Explorer' from VS Code Activity Bar
  Show 'AUTOMATION EXTENSIONS' view from VS Code Side Bar
  Choose the Edge browser and click the 'install' button

- In Visual Studio Code, Open the Command Palette: `Ctrl+Shift+P`
- Input or select: `Clicknium: Create Clicknium Project`
- Select project path, you can select or create one empty folder
  
Then project is created, you need to reference the cloud locator first:
Click 'Clicknium Explorer' from VS Code Activity Bar
Show 'CLOUD LOCATORS' view from VS Code Side Bar, click the 'reference' button on the right side of the locator store  
![locator ref](https://clickcorp.github.io/clicknium-docs/doc/img/locator_ref.png "locator ref")  

The default project contains two automation samples, one is Edge web automation, another is notepad automation.
```
from clicknium import clicknium as cc, locator, ui

def web_automation_demo():
  tab = cc.edge.open("https://www.bing.com/")
  tab.find_element(locator.new_store.bing.search_sb_form_q).set_text('clicknium')
  tab.find_element(locator.new_store.bing.svg).click()

  result_elements = tab.find_elements(locator.new_store.bing.a_search_result)
  for elem in result_elements:
    print(elem.get_text())
    elem.highlight(duration=1)

  tab.close()
```
```
from clicknium import clicknium as cc, locator, ui
import subprocess

def desktop_automation_demo():
  process = subprocess.Popen("notepad")
  ui(locator.new_store.notepad.document_15).set_text("clicknium")
  ui(locator.new_store.notepad.document_15).clear_text('controlclearvalue')
  process.kill()
```

- Run/debug the project
You can debug through `F5` or run through `Ctrl+F5`  
or Open the Command Palette: `Ctrl+Shift+P`:
Input or select: `Clicknium: Run` to run project or `Clicknium: Debug` to debug project


# Record UI Locators
In Visual Studio Code, press `Ctrl+F10` will invoke clicknium recorder and minimize current Visual Studio Code window.  
![clicknium recorder](https://clickcorp.github.io/clicknium-docs/doc/img/recorder_main.png)

After invoking Clicknium Recorder, you can move mouse on the target applicaiton, it will highlight the element recognized, 
if you want to capture the element, press `Ctrl` and click, the element locator will be added.

# Edit and Validate Locator
After recording the locators, you can open and edit the locator  
![clicknium VS code](https://clickcorp.github.io/clicknium-docs/doc/img/main.png) 
