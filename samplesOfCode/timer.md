```Python
"""
This function decrease the times each secondes
and ring a buzzer when the clock reaches 0
"""
def timer():
    global second_timer,minute_timer,color_index
    buzzer_active = False
    while timer_on:

        if minute_timer > 0 and second_timer > 0:
            time.sleep(1)
            second_timer -=1
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer > 0 and second_timer == 0:
            time.sleep(1)
            minute_timer -=1
            second_timer = (second_timer-1)%60
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer == 0 and second_timer > 0:
            time.sleep(1)
            second_timer -=1
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer == 0 and second_timer == 0:
            if not buzzer_active:
                display_time(minute_timer,second_timer,color_index)
                buzzer.duty(512)
                time.sleep(2)
                buzzer.duty(0)
                buzzer_active = True
            time.sleep(1)
```