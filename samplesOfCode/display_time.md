```Python
"""
This function displays the current time on the digital clock

@param hour			Current hour
@param minute		Current minute
@param color_index	Index that gives the information on which color to chose in the table colors
"""
def display_time(hour,minute,color_index):

    #Reset the clock by putting all led black corresponds to the number 8 on our device

    turn_off(0,8,0)
    turn_off(1,8,0)
    turn_off(2,8,0)
    turn_off(3,8,0)


    display_number(0,hour // 10,color_index)
    display_number(1,hour % 10,color_index)
    display_2points(4,color_index)
    display_number(2,minute // 10,color_index)
    display_number(3,minute % 10,color_index)
    np.write()
```