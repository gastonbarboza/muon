def escalafunc(threshold):
    if threshold < -.108:
        return(0.02)
    elif threshold <-.0539:
        return(0.01)
    elif threshold<-.0216:
        return(0.005)
    elif threshold < -.0108:
        return(0.002)
    else:
        return(0.001)
