```Python
def timer():
    global second_timer,minute_timer,color_index
    while timer_on:

        if minute_timer > 0 and second_timer > 0:
            sleep(1)
            second_timer -=1
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer > 0 and second_timer == 0:
            sleep(1)
            minute_timer -=1
            second_timer = (second_timer-1)%60
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer == 0 and second_timer > 0:
            time.sleep(1)
            second_timer -=1
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer == 0 and second_timer == 0:
            time.sleep(1)
            display_time(minute_timer,second_timer,color_index)
            buzzer.value(1)    
            time.sleep(2)
            buzzer.value(0)
```