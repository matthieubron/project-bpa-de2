from machine import Timer,Pin
import network
import urequests
import json
import machine
import neopixel
import time

# Configuration des NeoPixel

Num_PixelsLed = 14 #NE PAS OUBLIER DE CHANGER LE NB DE LED
PIN_NeoPixel = 25

np = neopixel.NeoPixel(machine.Pin(PIN_NeoPixel), Num_PixelsLed * 4)


#Configuration Boutons

button_color = Pin(27,Pin.IN,Pin.PULL_UP)



# Configuration Variables

hour = 0
minute = 0
second = 0


#Different colors for the display

colors = [(255,255,255),(127,0,255),(0,0,255),(0,255,0),(255,0,0)]
color_index = 0

#Creation of the dictionnary

Number_Leds = {
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
    #Probably a mistake here because of the 2 points that have 4 leds.
    2: { 
        0: [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        1: [32, 33, 34, 35],
        2: [30, 31, 32, 33, 36, 37, 38, 39, 40, 41],
        3: [30, 31, 32, 33, 34, 35, 36, 37, 40, 41],
        4: [28, 29, 32, 33, 34, 35, 40, 41],
        5: [28, 29, 30, 31, 34, 35, 36, 37, 40, 41],
        6: [28, 29, 30, 31, 34, 35, 36, 37, 38, 39, 40, 41],
        7: [30, 31, 32, 33, 34, 35],
        8: [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41],
        9: [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 40, 41]
    },
    3: {  
        0: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
        1: [46, 47, 48, 49],
        2: [44, 45, 46, 47, 50, 51, 52, 53, 54, 55],
        3: [44, 45, 46, 47, 48, 49, 50, 51, 54, 55],
        4: [42, 43, 46, 47, 48, 49, 54, 55],
        5: [42, 43, 44, 45, 48, 49, 50, 51, 54, 55],
        6: [42, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54, 55],
        7: [44, 45, 46, 47, 48, 49],
        8: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
        9: [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 54, 55]
    }
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
        hour = result.get("hour")
        minute = result.get("minute")
        second = result.get("seconds")
        print("Hour:", hour)
        print("Minute:", minute)
        print("Second:",second)
        
        # Fermer la réponse
        response.close()
        return hour, minute, second
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
    
    display_time(hour,minute,color_index)


# Modify the led to turn on
#number is for each neopixels, we control each of them one by one
#parameter number corresponds to the number to display on the neopixel (0-9)

def display_number(neopixel_index,number,color_index):
    
    start_index = neopixel_index * Num_PixelsLed #Where to start because in series
    leds = chiffres_leds.get(number,[]) #[] to avoid the crash if not find it will return []
    for led in leds:
        np[start_index + led] = colors[color_index]


#Modify the display on each NeoPixel

def display_time(hour,minute,color_index):
    
    display_number(3,hour // 10,color_index)
    display_number(2,hour % 10,color_index)
    display_number(1,minute // 10,color_index)
    display_number(0,minute % 10,color_index)
    np.write()


#Change the color to display


def change_color():
    
    global color_index
    if button_color.value() == 0:
        if color_index <= len(colors)-2: # "-2" bcs we're gonna add "1"
            color_index += 1
        else:
            color_index = 0
            
        
# Verification if button_color is pressed

button.irq(trigger = Pin.IRQ_FALLING, handler = change_color)



def main():
    
    connect_wifi()
    get_time()
    
    #Configuration of the timer
    timer = Timer(0)
    timer.init(period = 1000, mode = Timer.PERIODIC, callback = update_time)

    while True :
        pass 



