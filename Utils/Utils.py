import math
def get_direction(x1,x2,y1,y2):
    dx, dy = x1 - x2, y1 - y2
    dist = math.hypot(dx, dy)
    dx, dy = dx/dist, dy/dist
    return dx, dy

def normalize(value, min, max):
    return (value-min)/(max-min)
