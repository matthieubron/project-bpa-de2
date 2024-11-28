```Python
def alarm(hour, minute):
    if hour == alarm_h and minute == alarm_m:
        while buttonA.value() == 1 :
            buzzer.value(1)    
            time.sleep(1)
            buzzer.value(0)      
            time.sleep(1)
```