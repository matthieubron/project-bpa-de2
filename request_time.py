import requests
import json

# time_displayed = [0,0,0,0]

#print("Make the GET request")
response = requests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague") # Our local time
# response = requests.get("https://timeapi.io/api/time/current/zone?timeZone=Asia/Taipei")    # Friend's local time
#print(response.status_code)
result = json.loads(response.text) # convert string request into a dictionarry

hour = result.get("hour")
minute = result.get("minute")

# test to avoid index out of range (we should make a function)

def separating_numbers(hour, minute) :
    time_displayed = [0,0,0,0]
    if (hour < 10):
        time_displayed[0] = '0'
        time_displayed[1] = str(hour)[0]
        #print("Hour:", str(hour)[0])
    else :
        time_displayed[0] = str(hour)[0]
        time_displayed[1] = str(hour)[1]
        # print("Hour:", str(hour)[0])
        # print("Hour:", str(hour)[1])

    if (minute < 10):
        time_displayed[2] = '0'
        time_displayed[3] = str(minute)[0]
        # print("Minute:", str(minute)[0])
    else :
        time_displayed[2] = str(minute)[0]
        time_displayed[3] = str(minute)[1]
        # print("Minute:", str(minute)[0])
        # print("Minute:", str(minute)[1])
    return time_displayed


print(separating_numbers(hour, minute))

response.close() # Close the response to free up resources