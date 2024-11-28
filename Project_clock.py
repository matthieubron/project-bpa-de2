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

# Configuration des NeoPixel

Num_PixelsLed = 14 #NE PAS OUBLIER DE CHANGER LE NB DE LED
PIN_NeoPixel = 25

np = neopixel.NeoPixel(machine.Pin(PIN_NeoPixel), (Num_PixelsLed * 4) + 2)


# GPIO Configuration

buttonM = Pin(26,Pin.IN,Pin.PULL_UP)#jaune
buttonL = Pin(27,Pin.IN,Pin.PULL_UP)#blanc
buttonA = Pin(9,Pin.IN,Pin.PULL_UP) #rouge et temphumidity
buttonB = Pin(10,Pin.IN,Pin.PULL_UP) #vert
buttonC = Pin(13,Pin.IN,Pin.PULL_UP) #bleu

buzzer=Pin(23,Pin.OUT)

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor = DHT12(i2c)
ultrasonic = HCSR04(trigger_pin=5, echo_pin=12, echo_timeout_us=1000000)

# Variables Configuration
mode = 0

hour_req = 0
minute_req = 0
second_req = 0

hour = 0
minute =0
second=0

timer_on = False
timer_sec =0
minute_timer = 0
second_timer = 0

alarm_h = 0
alarm_m = 0
alarm_on = False

temp_digits = []
humidity_digits = []
display_mode = 0
#Different colors for the display

colors = [(255,255,255),(127,0,255),(0,0,255),(0,255,0),(255,0,0)]
colors_brightness=[(128,128,128),(64,0,128),(0,0,128),(0,128,0),(128,0,0)]
color_index = 0
turnoff_color = [(0,0,0)]
turnoff_color_index = 0

SSID = "telma"  # Remplacez par le nom de votre réseau Wi-Fi
PASSWORD = "01123581321"  # Remplacez par le mot de passe de votre Wi-Fi

#Creation of the dictionnary for the TimeZone

time_zone_index = 0
time_zone = [-7,+15,-8]

#Creation of the dictionnary for symbols

symbols_leds = {
    "celsius" : [0, 1, 2, 3, 8, 9, 10, 11],  
    "degree": [0, 1, 2, 3, 4, 5, 12, 13]   
}

#Creation of the dictionnary for the LED

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

# Connexion to the WIFI

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    print("Connexion au Wi-Fi...")
    while not wifi.isconnected():
        time.sleep(1)
    print("Connecté !")


# Request API to get the time

def get_time():
    print("Effectuer la requête GET")
    response = urequests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague")

    if response.status_code == 200:
        result = response.json()  # Utilise .json() pour charger directement en dict

        # Extraire l'heure et les minutes
        hour_req = result.get("hour")
        minute_req = result.get("minute")
        second_req = result.get("seconds")
        print("Hour:", hour_req)
        print("Minute:", minute_req)
        print("Second:",second_req)

        # Fermer la réponse
        response.close()
        return hour_req, minute_req, second_req
    else:
        print("Erreur lors de la requête:", response.status_code)
        response.close()
        return None, None, None

# Modify the time
# MANDATORY to put the parameter even if we don't use it so use timer or if only one "_"

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

# Modify the led to turn on
#number is for each neopixels, we control each of them one by one
#parameter number corresponds to the number to display on the neopixel (0-9)

def display_number(neopixel_index,number,color_index):
    
    leds = chiffres_leds[neopixel_index][number]#.get(number,[]) #[] to avoid the crash if not find it will return []
    distance = ultrasonic.distance_cm()
    print(distance, 'cm')
    if distance <= 5:
        #keep brightness of all seven segments high
        for led in leds:
            np[led] = colors[color_index]
    else:
        for led in leds:
            np[led] = colors_brightness[color_index]


def display_2points(two_points_index,color_index):
    
    leds = chiffres_leds.get(two_points_index,[]) #[] to avoid the crash if not find it will return []
    distance = ultrasonic.distance_cm()
    if distance<= 5:
        for led in leds:
            np[led] = colors[color_index]
    else:
        for led in leds:
            np[led] = colors_brightness[color_index]

def display_symbol(neopixel_index,number,color_index):
    
    leds = symbols_leds.get(symbol_name, [])
    for led in leds:
        np[led] = colors[color_index]

#Modify the display on each NeoPixel

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

def handle_debounced(pin, callback):
    global last_press_times
    current_time = time.ticks_ms()

    # Récupérer le dernier temps pour ce bouton, par défaut 0 s'il n'existe pas
    last_time = last_press_times.get(pin, 0)

    # Vérifier si le temps écoulé est suffisant
    if time.ticks_diff(current_time, last_time) > debounce_time:
        last_press_times[pin] = current_time  # Mettre à jour le dernier temps
        callback(pin)  # Appeler la fonction associée
        


def change_color(pin):
    global color_index, last_press_time

    #wait_pin_change(pin)

    print("Button pressed!")
    if buttonL.value() == 0:
        if color_index <= len(colors)-2: # "-2" bcs we're gonna add "1"
            color_index += 1
        else:
            color_index = 0



def turn_off(neopixel_index,number,turnoff_color_index): #UNE DES DEUX A SUPPRIMER

    leds = chiffres_leds[neopixel_index][number]
    for led in leds:
        np[led] = turnoff_color[turnoff_color_index]

def turn_off_simple(np):
    for i in range(len(np)):
        np[i] = (0,0,0)
    np.write()

def turn_off_2points(two_points_index):

    leds = chiffres_leds.get(two_points_index,[]) #[] to avoid the crash if not find it will return []
    for led in leds:
        np[led] = (0,0,0)    

#Je ne pense pas que ça va fonctionner sinon le faire en deux fonctions
#Mettre dans un premier temps avec les arguments etc et créer une deuxième fonction
#Sans argument qui sera appeler dans le handler du bouton

def convert_timezone(pin):
    global time_zone_index, hour, minute, color_index

    time_zone_index = (time_zone_index+1)%3
    shift = time_zone[time_zone_index]
    hour = (hour + shift) %24
    display_time(hour,minute,color_index)


def increment_alarm_h(pin):
    global alarm_h,alarm_m,color_index
    alarm_h = (alarm_h+1)%24
    display_time(alarm_h,alarm_m,color_index)


def increment_alarm_m(pin):
    global alarm_h,alarm_m,color_index
    alarm_m = (alarm_m+1)%24
    display_time(alarm_h,alarm_m,color_index)

def alarm_on_off(pin):
    global alarm_on
    alarm_on = not alarm_on
    if(alarm_on == True):
        display_2points(4,color_index)
    else :
        turn_off_2points(4)
x

def increment_minute(pin):
    global second_timer,minute_timer,color_index
    minute_timer = (minute_timer+1)%60
    display_time(minute_timer,second_timer,color_index)


def increment_second(pin):
    global second_timer,minute_timer,color_index
    second_timer = (second_timer+1)%60
    display_time(minute_timer,second_timer,color_index)




#Timer
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


def toggle_timer(pin):
    global timer_on

    if timer_on:
        timer_on = False
        print("Timer paused")
    else:
        timer_on = True
        _thread.start_new_thread(timer,())


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

def alarm(hour, minute):
    if hour == alarm_h and minute == alarm_m:
        while buttonA.value() == 1 :
            buzzer.value(1)    
            time.sleep(1)
            buzzer.value(0)      
            time.sleep(1)

def getTemperatureAndHumidity():
        
    global temp_digits
    global humidity_digits
    
    temp_digits = []
    humidity_digits = []

    temperature, humidity = sensor.read_values()
        
    humidity_str = f"{humidity:.2f}"
    temp_str = f"{temperature:.2f}"
        
    for d in temp_str:
        if d.isdigit():
            temp_digits.append(int(d))

    for d in humidity_str:
        if d.isdigit():
            humidity_digits.append(int(d))
               
def display_change():
        
    global display_mode
    if  display_mode==0:
        getTemperatureAndHumidity()
        display_number(3,temp_digits[0],color_index)
        display_number(2,temp_digits[1],color_index)
        display_symbol(1,"degree",color_index)
        display_symbol(0,"celsius",color_index)
        np.write()
        display_mode = 1
        time.sleep(0.2) 
    elif display_mode==1:
        getTemperatureAndHumidity()
        display_number(3,humidity_digits[0],color_index)
        display_number(2,humidity_digits[1],color_index)
        display_number(1,humidity_digits[2],color_index)
        display_number(0,humidity_digits[3],color_index)
        np.write()
        display_mode = 0
        time.sleep(0.2)
            
#Return an integer between 0 an 3 corresponding to the 4 differents states of the clock
def statemode():
    global mode
    mode = (mode + 1)%4
    return mode

def state():
    #Display curent Time
    if (statemode() == 0):
        print("mode 0")
        #Display Time
        display_time(hour,minute,color_index)
        if (alarm_on == True):
            alarm(hour,minute)
        #change time zone
        buttonB.irq(trigger = Pin.IRQ_FALLING, handler = lambda pin: handle_debounced(pin, convert_timezone))
        # Switch on / off alarm
        

    #Set and display alarm time
    elif (statemode() == 1): # Alarm
        print("mode 1")
        display_time(alarm_h, alarm_m, color_index)
        buttonB.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,increment_alarm_h))
        buttonC.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin,increment_alarm_m))
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
        # All function who need to run in background
        state()
        pass
    
    
buttonL.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, change_color))
buttonM.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, statemode))
