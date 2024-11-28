```Python
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
```