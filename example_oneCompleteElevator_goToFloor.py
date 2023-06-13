## This example was created by a student.

SENSOR_ACURACY = 0.01

def goToFloor(e, eleId, floorNumber):
    pos = e.getPosition(eleId)
    speed = e.getSpeed(eleId)
    step = e.getDescription(eleId)['speedStep']
    if speed <=0:
        step = step *(-1)
    t = abs(speed / step) 
    math = speed*t - step*(t**2)/2
    if floorNumber-SENSOR_ACURACY<pos<floorNumber+SENSOR_ACURACY and -abs(step)<speed<abs(step):
        return True
    else:
        if math+pos < floorNumber:
            e.speedUp(eleId)
            return False
        elif math+pos > floorNumber:
            e.speedDown(eleId)
            return False
