```Python
"""
This function takes care of the incrementation of the time
and uses display_time to show the values on the digital clock

@param _	Identify the pin that triggered the interruption
"""
def update_time(_):
    global hour,minute,second
    second +=1
    if second >=60:
        second = 0
        minute +=1
    if minute >=60:
        minute = 0
        hour +=1
    if hour >=24:
        hour = 0
```