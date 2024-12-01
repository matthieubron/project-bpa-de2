```Python
"""
This function sends a request to connect to the wifi using SSID and PASSWORD
"""
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    print("Connexion au Wi-Fi...")
    while not wifi.isconnected():
        time.sleep(1)
    print("Connecté !")
```