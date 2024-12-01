```Python
"""
This function triggers the buzzer when the curent time is equals to alarm time 

@param hour		Current hour
@param	minute	Current minute
"""
def alarm(hour, minute):
    global alarm_on
    if hour == alarm_h and minute == alarm_m and alarm_on:
        for i in range(5):
            display_time(hour,minute,color_index)
            buzzer.duty(512)
            time.sleep(1)
            buzzer.duty(0)
            time.sleep(1)
        alarm_on = False
```