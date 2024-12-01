from machine import Timer,Pin,I2C
import network
import urequests
import json
import machine
import neopixel
import time
import _thread
from CaptorsConfig import DHT12
from sh1106 import SH1106_I2C
from CaptorsConfig import HCSR04

Num_PixelsLed = 14 
PIN_NeoPixel = 25

np = neopixel.NeoPixel(machine.Pin(PIN_NeoPixel), (Num_PixelsLed * 4) + 2)

ultrasonic = HCSR04(trigger_pin=5, echo_pin=12, echo_timeout_us=1000000)

mode = 0

hour_req = 0
minute_req = 0
second_req = 0

hour = 0
minute =0
second=0

colors = [(255,255,255),(127,0,255),(0,0,255),(0,255,0),(255,0,0)]
colors_brightness=[(128,128,128),(64,0,128),(0,0,128),(0,128,0),(128,0,0)]
color_index = 0
turnoff_color = [(0,0,0)]
turnoff_color_index = 0

SSID = "telma"  
PASSWORD = "01123581321"

chiffres_leds = {
    0: {  
        0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        1: [4, 5, 6, 7],
        2: [2, 3, 4, 5, 8, 9, 10, 11, 12, 13],
        3: [2, 3, 4, 5, 6, 7, 8, 9, 12, 13],
        4: [0, 1, 4, 5, 6, 7, 12, 13],
        5: [0, 1, 2, 3, 6, 7, 8, 9, 12, 13],
        6: [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13],
        7: [2, 3, 4, 5, 6, 7],
        8: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        9: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13]
    },
    1: {
        0: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        1: [18, 19, 20, 21],
        2: [16, 17, 18, 19, 22, 23, 24, 25, 26, 27],
        3: [16, 17, 18, 19, 20, 21, 22, 23, 26, 27],
        4: [14, 15, 18, 19, 20, 21, 26, 27],
        5: [14, 15, 16, 17, 20, 21, 22, 23, 26, 27],
        6: [14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27],
        7: [16, 17, 18, 19, 20, 21],
        8: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        9: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27]
    },
    2: {
        0: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41],
        1: [34, 35, 36, 37],
        2: [32, 33, 34, 35, 38, 39, 40, 41, 42, 43],
        3: [32, 33, 34, 35, 36, 37, 38, 39, 42, 43],
        4: [30, 31, 34, 35, 36, 37, 42, 43],
        5: [30, 31, 32, 33, 36, 37, 38, 39, 42, 43],
        6: [30, 31, 32, 33, 36, 37, 38, 39, 40, 41, 42, 43],
        7: [32, 33, 34, 35, 36, 37],
        8: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
        9: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43]
    },
    3: {
        0: [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
        1: [48, 49, 50, 51],
        2: [46, 47, 48, 49, 52, 53, 54, 55, 56, 57],
        3: [46, 47, 48, 49, 50, 51, 52, 53, 56, 57],
        4: [44, 45, 48, 49, 50, 51, 56, 57],
        5: [44, 45, 46, 47, 50, 51, 52, 53, 56, 57],
        6: [44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57],
        7: [46, 47, 48, 49, 50, 51],
        8: [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57],
        9: [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 57]

    },
    4 : [28,29]

}

"""
This function send a request to connect to the wifi using SSID and PASSWORD
"""
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    print("Connexion au Wi-Fi...")
    while not wifi.isconnected():
        time.sleep(1)
    print("Connecté !")

"""
This function send a request to get the current time and put it in the different variables
"""
def get_time():
    print("Effectuer la requête GET")
    response = urequests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague")

    if response.status_code == 200:
        result = response.json() 

        hour_req = result.get("hour")
        minute_req = result.get("minute")
        second_req = result.get("seconds")
        print("Hour:", hour_req)
        print("Minute:", minute_req)
        print("Second:",second_req)

        response.close()
        return hour_req, minute_req, second_req
    else:
        print("Erreur lors de la requête:", response.status_code)
        response.close()
        return None, None, None

"""
This function take care of the incrementation of the time and use display_time to show the values on the digital clock
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
    print(hour)
    print(minute)
    print(second)
    display_time(hour,minute,color_index)

"""
This function is used for displaying specific number on Leds

@param neopixel_index		Indicates on which neopixel led the number should be display
@param number				Refers to the number in the dictionnary that corresponds to a segment of Leds
@param color_index			Tells which color to chose in the table colors or colors_brightness, depending on the distance detected
"""

def display_number(neopixel_index,number,color_index):
    
    
    leds = chiffres_leds[neopixel_index][number]
    distance = ultrasonic.distance_cm()
    time.sleep_ms(10)
    print(distance, 'cm')
    if distance <= 5:
        for led in leds:
            np[led] = colors[color_index]
    else:
        for led in leds:
            np[led] = colors_brightness[color_index]

"""
This function is used for controlling the display of the two points

@param two_points		Refers to the two Leds that control the two points on the clock
@param color_index		Tells which color to chose in the table colors or colors_brightness, depending on the distance detected
"""
def display_2points(two_points_index,color_index):
    
    leds = chiffres_leds.get(two_points_index,[]) 
    distance = ultrasonic.distance_cm()
    if distance<= 5:
        for led in leds:
            np[led] = colors[color_index]
    else:
        for led in leds:
            np[led] = colors_brightness[color_index]
            
"""
This function is used for displaying specific symbol on Leds

@param neopixel_index		Indicates on which neopixel led the number should be display
@param number				Refers to the number in the dictionnary that corresponds to a segment of
@param color_index			Tells which color to chose in the table colors or colors_brightness, depending on the distance detected
"""
def display_symbol(neopixel_index,number,color_index):
    
    leds = symbols_leds.get(symbol_name, [])
    for led in leds:
        np[led] = colors[color_index]

"""
This function display the current time on the digital clock

@param hour			Current hour
@param minute		Current minute
@param color_index	Tells which color to chose in the table colors or colors_brightness, depending on the distance detected
"""
def display_time(hour,minute,color_index):

    #Reset the clock by putting all led black corresponds to the number 8 on our device

    #display_number(0,8,5)
    #display_number(1,8,5)
    #display_number(2,8,5)
    #display_number(3,8,5)

    turn_off(0,8,0)
    turn_off(1,8,0)
    turn_off(2,8,0)
    turn_off(3,8,0)

    #OR

    #turn_off_simple(np)

    display_number(0,hour // 10,color_index)
    display_number(1,hour % 10,color_index)
    display_2points(4,color_index)
    display_number(2,minute // 10,color_index)
    display_number(3,minute % 10,color_index)
    np.write()


#Change the color to display


last_press_times = {}  # Dictionnaire pour suivre les derniers temps d'appui de chaque bouton
debounce_time = 200

"""
This function make sure that there is no boucne when we press a button

@param pin		correspond to the pin of the button
@param callback	call tha associated function
"""
def handle_debounced(pin, callback):
    global last_press_times
    current_time = time.ticks_ms()

    # Récupérer le dernier temps pour ce bouton, par défaut 0 s'il n'existe pas
    last_time = last_press_times.get(pin, 0)

    # Vérifier si le temps écoulé est suffisant
    if time.ticks_diff(current_time, last_time) > debounce_time:
        last_press_times[pin] = current_time  # Mettre à jour le dernier temps
        callback(pin)  # Appeler la fonction associée

"""
This function turn off all the Leds

@param neopixel_index		Indicates on which neopixel led the number should be display
@param number				Refers to the number in the dictionnary that corresponds to a segment of Leds
@param turnoff_color_index	Indicates which color need to be shutdownx²
"""
def turn_off(neopixel_index,number,turnoff_color_index): #UNE DES DEUX A SUPPRIMER

    leds = chiffres_leds[neopixel_index][number]
    for led in leds:
        np[led] = turnoff_color[turnoff_color_index]

"""
This function turn off the Leds of the two points

@param two_points_index		Refers to the number of Leds of the two points
"""
def turn_off_2points(two_points_index):

    leds = chiffres_leds.get(two_points_index,[]) #[] to avoid the crash if not find it will return []
    for led in leds:
        np[led] = (0,0,0)
     
"""
This function increase the minute of the timer

@param pin	Identify the pin that triggered the interruption
"""
def increment_minute(pin):
    global second_timer,minute_timer,color_index
    minute_timer = (minute_timer+1)%60
    display_time(minute_timer,second_timer,color_index)

"""
This function increase the second of the timer

@param pin	Identify the pin that triggered the interruption
"""
def increment_second(pin):
    global second_timer,minute_timer,color_index
    second_timer = (second_timer+1)%60
    display_time(minute_timer,second_timer,color_index)

def main():
    #Time request
    global hour,minute,second,mode
    connect_wifi()
    hour_req,minute_req,second_req = get_time()
    hour = hour_req
    minute = minute_req
    second = second_req

    timer = Timer(0)
    timer.init(period = 1000, mode = Timer.PERIODIC, callback = update_time)
    
    while True :
        pass