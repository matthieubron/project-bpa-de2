# Project BPA DE2 : Clock

* [Part 1: Showing current time](#CurentTime)
* [Part 2: Alarm Clock](#AlarmClock)

### Team Members

* BERMAN Noam (responsible for code)
* BRON Matthieu (responsible for github)
* CLOUARD Adam (responsible for documentation)

### Implementations

* Showing current time
* Alarm clock
* Light mode base on distance
* Change Time color
* Temperature and humidity sensor
* Time zones
* <em>Automatic night mode base on time</em>
* <em>Timer</em>

### Hardware description

* ESP32 board with pre-installed MicroPython firmware, USB cable
* Breadboard
* 5 Push button
* 4 NeoPixel displays
* Proximity sensor
* Jumper wires
* Temperature and humidity sensor

### Software description
<u>Include flowcharts of your algorithm(s) and direct links to the source files.Present the modules you used in the project</u>

Flowshart of digital clock

<u>je pense qu'il faut supprimer le flowchart, ou alors faire une machine à état avec des cercles </u>

![Flow_chart_digital_clock](Pictures/flowchart_digital_clock.drawio.svg)



* [Display current time](#CurentTime) <u>link to py </u>
* [Alarm Clock](#AlarmClock) <u>link to py </u>
* [Light based on distance](#LightDistance) <u>link to py </u>

### Instructions and photos
Wiring of digital clock

![schema_gpio](Pictures/schema_gpio.svg)

Different states of the alarm clock


| Button / Mode                 |   M (yellow)  |   L (white) |   A (red)                 |   B (green)       |   C (blue)           |
| :----:                        | :----:        | :----:      | :----:                    | :----:            | :----:               | 
| Display curent time           | Mode          | Light       |Stop alarm                 | Change time zone  | -                    |
| Set Alarm                     | Mode          | Light       |Switch On/Off alarm        | Increase hours    | Increase minutes     |
| Set Timer                     | Mode          | Light       |Start Timer                | Increase minutes  | Increase seconds     |
| Display Trmperature & humidity| Mode          | Light       |Change temperature/humidity| -                 |      -               |  


States are defined thanks to the function `state()`.
```Python
def state():
    #Display curent Time
    if (statemode() == 0):
        print("mode 0")
        #Display Time
        display_time(hour,minute,color_index)
        if (AlarmOn == True):
            alarm(hour,minute)
        #change time zone
        buttonB.irq(trigger = Pin.IRQ_FALLING, handler = lambda pin: handle_debounced(pin, convert_timezone))
        # Switch on / off alarm
        

    #Set and display alarm time
    elif (statemode() == 1): # Alarm
        print("mode 1")
        display_time(alarmH, alarmM, color_index)
        buttonB.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,increment_AlarmH))
        buttonC.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,increment_AlarmM))
        buttonA.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,alarm_on_off))

    # Set and display timer
    elif (statemode() == 2):
        print("mode 2")
        display_time(minute_timer, second_timer, color_index)
        buttonC.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,increment_second))
        buttonB.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,increment_minute))
        #/!\ pas sûr pour de l'appel de fonction
        buttonA.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,toggle_timer))

    elif (statemode() == 3):
        print("mode 3")
        buttonA.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,display_change))
```

Schematic of the NeoPixel display, we set a dictionary

![NeoPixel_schematic](Pictures/NeoPixel_schematics.svg)


<a name="CurentTime"></a>

## Display current time



<a name="AlarmClock"></a>

## Alarm clock

<a name="LightDistance"></a>

## Change brightness according to distance



### References and tools

* API current time request [timeapi.io](https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague)
* Use a dictionarry in Python [w3schools.com](https://www.w3schools.com/python/python_dictionaries_access.asp) and convert string into a dictionarry [geeksforgeeks.org](https://www.geeksforgeeks.org/python-convert-string-dictionary-to-dictionary/)
* Acces one specific char of a strig [computerscienced.co](https://computerscienced.co.uk/site/knowledge-base/how-do-i-get-the-first-letter-of-a-string-in-python/)
* To know RGB color codes [rapidtables.com](https://www.rapidtables.com/web/color/RGB_Color.html)
* Functions linked to pin class [micropython.org](https://docs.micropython.org/en/latest/library/machine.Pin.html)
