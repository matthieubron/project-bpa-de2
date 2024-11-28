```Python
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
```