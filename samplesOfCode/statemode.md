```Python
"""
This function takes care of which mode is currently used
and call a function that configure the button depending on the mode

@param pin	Identify the pin that triggered the interruption
"""
def statemode(pin):
    global mode
    mode = (mode + 1)%4
    print(mode)
    configure_buttons()
```