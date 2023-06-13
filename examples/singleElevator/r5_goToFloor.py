ODCHYLKA = 0.01

def goToFloor(e, idVytahu, floorNumber):
    pos = e.getPosition(idVytahu)
    speed = e.getSpeed(idVytahu)
    step = e.getDescription(idVytahu)['speedStep']
    if speed <=0:
        step = step *(-1)
    t = abs(speed / step) 
    math = speed*t - step*(t**2)/2


    if floorNumber-ODCHYLKA<pos<floorNumber+ODCHYLKA and -abs(step)<speed<abs(step):
        return True
    else:
        if math+pos < floorNumber:
            e.speedUp(idVytahu)
            return False
        elif math+pos > floorNumber:
            e.speedDown(idVytahu)
            return False
  


