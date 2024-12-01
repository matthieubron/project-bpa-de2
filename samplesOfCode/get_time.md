```Python
"""
This function sends a request to get the current time
and puts it in the different variables

@return		hours_req		the current hour
@return		minute_req		the courrent minute
@return		second_req		the current seconde
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
```