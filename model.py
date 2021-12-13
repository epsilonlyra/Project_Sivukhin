import numpy as np
import math
import pygame

BLUE = 0x0000FF
BLACK = 0x000000
WHITE = 0xFFFFFF
rho_0 = 10
speed = 0.5
h = 5
g = 5
r_ball = 6
m = 1

k = 100         # параметры для уравнения состояния
power = 35
nu = 0.2
dt = 0.2


def W(x, y, h):
    '''
    Gausssian Smoothing kernel (2D)
    x, y - вектора координат
    h - глубина сглаживния
    '''

    # попытка поменять kernel на более адекватный
    r = np.sqrt(x**2 + y**2)
    w = (1.0 / (h*np.sqrt(np.pi)))**3 * np.exp( -r**2 / h**2)
    return w
	
	
def gradW(x, y, h):
    '''
    Gradient of the Gausssian Smoothing kernel (2D)
    x, y - вектора координат
    h - глубина сглаживния
    '''

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

def Pressure(rho):
    '''
    Возвращает давление
    '''
    p = k * rho**(1+1/power)

    return p

def Acceleration(r, v, m, h, nu):
    '''
    Возвращает ускорение частиц
    '''
    rho = Density(r, m, h)
    p = Pressure(rho)
    dx, dy = RelativeCoordinates(r)
    dWx, dWy = gradW(dx, dy, h)

    ax = -np.sum(m * (p/rho**2 + p.T/rho.T**2) * dWx, 1)
    ay = -np.sum(m * (p/rho**2 + p.T/rho.T**2) * dWy, 1)
    ay += g
    a = np.array([ax, ay])
    a = a.T
    a -= nu * v

    return a

def reflect(vx, vy, alpha):
    '''
    vx, vy - координаты скорости
    alpha - угол
    '''
    u = vy * math.cos(alpha) - vx * math.sin(alpha)
    w = vx * math.cos(alpha) + vy * math.sin(alpha)

    k = 1
    ux = -u * math.sin(alpha) - k*w * math.cos(alpha)
    uy = u * math.cos(alpha) - k*w * math.sin(alpha)

    return ux, uy

def make_water(left, right, up, down, N):
    x = np.random.randint(left, (right+left)/2, N).astype(np.float64)
    y = np.random.randint((up+down)/2, down, N).astype(np.float64)
    r = np.array([x, y]).T
    v = np.zeros(r.shape)

    return r, v

def step(r, v):
    rho = Density(r, m, h)
    acc = Acceleration(r, v, m, h, nu)
    
    v += acc * dt
    r += v * dt

    return r, v

    


if __name__ == "__main__":
    example()
    

pygame.quit()











        
