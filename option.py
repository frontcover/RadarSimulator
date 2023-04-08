class Option:
    ################ Left radar ##################
    # CFAR parameters
    enable_CFAR = False     # cfar on or off
    pfa = 0.01              # cfar's probability of false alarm
    train_size = 5
    guard_size = 1
    
    # Other parameters
    v_multiple = 10     # velocity multiplier

    ################ Right radar ##################
    show_actual = False
    show_observe = False
    show_predict = True
