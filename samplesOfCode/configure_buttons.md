```Python
"""
This function configures the button depending on the current mode the user is,
so that a button can be configure for different function depending on the mode
"""
def configure_buttons():
    global mode
    buttonA.irq(handler=None)
    buttonB.irq(handler=None)
    buttonC.irq(handler=None)

    if mode == 0:
        buttonB.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, convert_timezone))

    elif mode == 1:
        buttonA.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, alarm_on_off))
        buttonB.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_alarm_h))
        buttonC.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_alarm_m))

    elif mode == 2:
        buttonA.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, toggle_timer))
        buttonB.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_minute))
        buttonC.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_second))

    elif mode == 3:
        buttonA.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, display_change))

```