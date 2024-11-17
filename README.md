# Project BPA DE2 : Clock

* [Part 1: Showing current time](#CurentTime)
* [Part 2: Alarm Clock](#AlarmClock)

### Team Members

* BERMAN Noam (responsible for code)
* BRON Matthieu (responsible for github)
* CLOUARD Adam (responsible for documentation)

### Implementations

* Showing curent time
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
* 4 Push button
* 4 pull-up resistors
* 4 NeoPixel displays
* Proximity sensor
* Jumper wires
* Temperature and humidity sensor

### Software description
<u>Include flowcharts of your algorithm(s) and direct links to the source files.Present the modules you used in the project</u>

Flowshart of digital clock

![Flow_chart_digital_clock](Pictures/flowchart_digital_clock.drawio.svg)

* [Alarm Clock](#AlarmClock)

### Instructions and photos
Wiring of digital clock

![schema_gpio](Pictures/schema_gpio.svg)



Schematic of the NeoPixel display, we set a dictionary

![NeoPixel_schematic](Pictures/NeoPixel_schematics.svg)


<a name="CurentTime"></a>

## Showing curent time



<a name="AlarmClock"></a>

## Alarm clock




### References and tools

* API current time request [timeapi.io](https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague)
* Use a dictionarry in Python [w3schools.com](https://www.w3schools.com/python/python_dictionaries_access.asp) and convert string into a dictionarry [geeksforgeeks.org](https://www.geeksforgeeks.org/python-convert-string-dictionary-to-dictionary/)
* Acces one specific char of a strig [computerscienced.co](https://computerscienced.co.uk/site/knowledge-base/how-do-i-get-the-first-letter-of-a-string-in-python/)
* To know RGB color codes [rapidtables.com](https://www.rapidtables.com/web/color/RGB_Color.html)
* Functions linked to pin class [micropython.org](https://docs.micropython.org/en/latest/library/machine.Pin.html)