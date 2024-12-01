```Python
"""
This function initiates what the clock doesat the beginning of each mode
of the clock
"""
def state():
    if (mode == 0):
        display_time(hour,minute,color_index)

    elif (mode == 1):
        display_time(alarm_h, alarm_m, color_index)

    elif (mode == 2):
        display_time(minute_timer, second_timer, color_index)

    elif (mode == 3):

        pass
```