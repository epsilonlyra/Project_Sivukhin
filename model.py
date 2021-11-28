import numpy as np
import pygame

BLUE = 0x0000FF
BLACK = 0x000000
WHITE = 0xFFFFFF
rho_0 = 2
speed = 10
h = 5
g = 10

def W(x, y, h ):
    """
    Gausssian Smoothing kernel (3D)
    x     is a vector/matrix of x positions
    y     is a vector/matrix of y positions
    z     is a vector/matrix of z positions
    h     is the smoothing length
    w     is the evaluated smoothing function
    """
    
    '''w = np.zeros(x.shape)
    k = 15/(7*np.pi*h**2)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            r = np.sqrt(x[i][j]**2 + y[i][j]**2)
            xi = r/h
            if xi < 1:
                w[i][j] = (1-3/2*xi**2+3/4*xi**3)*k
            elif xi < 2:
                w[i][j] = (2-xi**3)/6*k
            else:
                w[i][j] = 0'''
    r = np.sqrt(x**2 + y**2)
    w = (1.0 / (h*np.sqrt(np.pi)))**3 * np.exp( -r**2 / h**2)
    return w
	
	
def gradW(x, y, h ):
    """
    Gradient of the Gausssian Smoothing kernel (3D)
    x     is a vector/matrix of x positions
    y     is a vector/matrix of y positions
    z     is a vector/matrix of z positions
    h     is the smoothing length
    wx, wy, wz     is the evaluated gradient
    """
    wx = np.zeros(x.shape)
    wy = np.zeros(y.shape)
    k = 15/(7*np.pi*h**2)

    '''for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            r = np.sqrt(x[i][j]**2 + y[i][j]**2)
            xi = (x[i][j]**2 + y[i][j]**2)**(0.5)/h
            if (x[i][j] == 0) and (y[i][j] == 0):
                wx[i][j], wy[i][j] = 0, 0
            if xi < 1:
                wx[i][j] = 0
                wx[i][j], wy[i][j] = k*x[i][j]/(h*r)*(-3*xi + 9/4*xi**2), k*y[i][j]/(h*r)*(-3*xi + 9/4*xi**2)
            elif xi < 2:
                wx[i][j], wy[i][j] = k*x[i][j]/(h*r)*(-xi**2/2), k*y[i][j]/(h*r)*(-xi**2/2)
            else:
                wx[i][j], wy[i][j] = 0, 0'''

    r = np.sqrt(x**2 + y**2)
    
    n = -2 * np.exp( -r**2 / h**2) / h**5 / (np.pi)**(3/2)
    wx = n * x
    wy = n * y
    
    return wx, wy



def RelativeCoordinates(r):
    '''
    Дает относительные координаты j-й частицы относительно i-й
    r - матрица nx2
    '''
    M = r.shape[0]
    rx = r[:,0].reshape((M, 1))
    ry = r[:,1].reshape((M, 1))

    dx = rx - rx.T
    dy = ry - ry.T
    
    return dx, dy

def Density(r, m, h):
    '''
    Возвращает плотность в местах нахождения частиц
    r - матрица nx2 координат частиц
    m - масса частиц
    h - глубина сглаживания
    '''

    dx, dy = RelativeCoordinates(r)
    M = r.shape[0]
    rho = np.sum(m * W(dx, dy, h), 1).reshape((M, 1))
    
    return rho

def Pressure(rho, k, n):
    '''
    Возвращает давление
    '''

    p = k * rho**(1+1/n)
    #p = speed**2*(rho-rho_0)

    return p

def Acceleration(r, v, m, h, k, n, nu):
    '''
    Возвращает ускорение частиц
    '''
    rho = Density(r, m, h)
    p = Pressure(rho, k, n)
    dx, dy = RelativeCoordinates(r)
    dWx, dWy = gradW(dx, dy, h)

    ax = -np.sum(m * (p/rho**2 + p.T/rho.T**2) * dWx, 1)
    ay = -np.sum(m * (p/rho**2 + p.T/rho.T**2) * dWy, 1)

    

    ay += g

    
        
    a = np.array([ax, ay])
    a = a.T


    a -= nu * v

    return a



def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    
    N = 400
    t = 0
    dt = 0.2

    s = 30          # ширина прямоугольника
    left = 100      # левая граница     (int)
    right = 500     # правая граница
    up = 100        # верхняя граница
    down = 500      # нижняя граница
    k = 100         # параметры для уравнения состояния
    n = 35
    nu = 0.2

    m = 1
    
    x = np.random.randint(left, (right+left)/2, N).astype(np.float64)
    y = np.random.randint((up+down)/2, down, N).astype(np.float64)
    r = np.array([x, y]).T
    v = np.zeros(r.shape)

    acc = Acceleration(r, v, m, h, k, n, nu)

    while True:
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (left, down, right-left, s))
        for el in r:
            x, y = el
            pygame.draw.circle(screen, BLUE, (x, y), 6)
        pygame.display.update()
        v += acc * dt
        r += v * dt
        t += dt

        for i in range(N):
            x, y = r[i]
            if x < left:
                r[i][0] = left
                v[i][0] = - v[i][0]
            if x > right:
                r[i][0] = right
                v[i][0] = - v[i][0]
            if y < up:
                r[i][1] = up
                v[i][1] = - v[i][1]
            if y > down:
                r[i][1] = down
                v[i][1] = - abs(v[i][1])
        
                

        rho = Density(r, m, h)
        acc = Acceleration(r, v, m, h, k, n, nu)
    

main()
    











        
