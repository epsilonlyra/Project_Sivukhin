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

gamma = 7

death = False

def W(x, y, h ):
    '''
    Gausssian Smoothing kernel (2D)
    x, y - вектора координат
    h - глубина сглаживния
    '''

    # попытка поменять kernel на более адекватный
    if death:
        w = np.zeros(x.shape)
        k = 15/(7*np.pi*h**2)
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                r = np.sqrt(x[i][j]**2 + y[i][j]**2)
                xi = r/h
                if xi < 1:
                    w[i][j] = (2/3 - xi**2 + 1/2*xi**3)*k
                elif xi < 2:
                    w[i][j] = (2 - xi)**3/6*k
                else:
                    w[i][j] = 0
    
    else:
        r = np.sqrt(x**2 + y**2)
        w = (1.0 / (h*np.sqrt(np.pi)))**3 * np.exp( -r**2 / h**2)
    return w
	
	
def gradW(x, y, h ):
    '''
    Gradient of the Gausssian Smoothing kernel (2D)
    x, y - вектора координат
    h - глубина сглаживния
    '''
    wx = np.zeros(x.shape)
    wy = np.zeros(y.shape)
    k = 15/(7*np.pi*h**2)

    if death:
        for i in range(x.shape[0]):
            for j in range(y.shape[0]):
                rr = math.sqrt(x[i][j]**2 + y[i][j]**2)
                xi = rr/h
                if (x[i][j] == 0) and (y[i][j] == 0):
                    wx[i][j], wy[i][j] = 0, 0
                elif xi < 1:
                    wx[i][j], wy[i][j] = k*x[i][j]/(h*rr)*(-2*xi + 3/2*xi**2), k*y[i][j]/(h*rr)*(-2*xi + 3/2*xi**2)
                elif xi < 2:
                    wx[i][j], wy[i][j] = k*x[i][j]/(h*rr)*(-(2-xi)**2/2), k*y[i][j]/(h*rr)*(-(2-xi)**2/2)
                else:
                    wx[i][j], wy[i][j] = 0, 0

    else:
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

    #p = rho_0 * speed**2 * ((rho/rho_0)**gamma - 1) / gamma
    p = k * rho**(1+1/power)
    #p = speed**2*(rho-rho_0)

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

    k = 0.6
    ux = -u * math.sin(alpha) - k*w * math.cos(alpha)
    uy = u * math.cos(alpha) - k*w * math.sin(alpha)
    #if True:
    #    uu = 
    return ux, uy





def example():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    
    N = 800
    t = 0
    dt = 0.2

    s = 30          # ширина прямоугольника
    left = 100      # левая граница     (int)
    right = 500     # правая граница
    up = 100        # верхняя граница
    down = 500      # нижняя граница
    nu = 0.2
    alpha = -2

    m = 1
    
    x = np.random.randint(left, (right+left)/2, N).astype(np.float64)
    y = np.random.randint((up+down)/2, down, N).astype(np.float64)
    r = np.array([x, y]).T
    v = np.zeros(r.shape)

    acc = Acceleration(r, v, m, h, nu)

    finished = False
    inclined = True
    
    while not finished:
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (left, down, right-left, s))
        v += acc * dt
        r += v * dt
        t += dt
                
        # checking collisions with walls and drawing them
        if inclined:
            pygame.draw.line(screen, WHITE, (left, down),
                             (right, right - (right-left)/math.tan(alpha)), width = 1)
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
                if y > down - (x-left)/math.tan(alpha):
                    r[i][1] = down - (x-left)/math.tan(alpha)
                    v[i][0], v[i][1] = reflect(v[i][0], v[i][1], alpha)

        else:
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
                    v[i][1] = - v[i][1]

        # drawing water
        for el in r:
            x, y = el
            pygame.draw.circle(screen, BLUE, (x, y), r_ball)
        pygame.display.update()

        rho = Density(r, m, h)
        acc = Acceleration(r, v, m, h, nu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

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











        
