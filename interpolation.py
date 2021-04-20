
def getY(x1, x2, y1, y2, x):
    m = (y1-y2)/(x1-x2)
    n = y1 - (m*x1)

    return (m*x + n)

def getX(x1, x2, y1, y2, y):
    m = (y1-y2)/(x1-x2)
    n = y1 - (m*x1)

    return (y-n)/m


x1 = 0.9481
y1 = 276.46

x2 = 0.9803
y2 = 286.71

x = 0.9724


print('\n------------------------')
print(getY(x1,x2,y1,y2,x))
print('------------------------\n')

