```Python
"""
This function allows the user to switch between the temperature mode
and the humidity mode and call a function to display it on the clock

@param pin	Identify the pin that triggered the interruption
"""
def display_change(pin):

    global display_mode
    print(display_mode)

    turn_off(0,8,0)
    turn_off(1,8,0)
    turn_off(2,8,0)
    turn_off(3,8,0)

    if  display_mode == 0:
        display_change_temp()
    else:
        display_change_humidity()
```