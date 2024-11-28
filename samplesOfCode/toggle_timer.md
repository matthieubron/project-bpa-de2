```Python
def toggle_timer(pin):
    global timer_on

    if timer_on:
        timer_on = False
        print("Timer paused")
    else:
        timer_on = True
        _thread.start_new_thread(timer,())
```