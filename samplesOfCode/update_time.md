```Python
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
    print(hour)
    print(minute)
    print(second)
    display_time(hour,minute,color_index)
```