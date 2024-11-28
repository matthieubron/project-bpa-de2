```Python
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
```