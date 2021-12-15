import math
import numpy as np


# parameters for smoothing and particles
h = 5   # smoothing depth
m = 1   # particle mass
g = 5   # free fall acceleration

# parameters for state equation
k = 100
power = 35
nu = 0.2
dt = 0.2


def kernel(x, y):
    """
    Gausssian Smoothing kernel (2D)
    x, y - coordinates
    h - smoothing depths
    """

    r = np.sqrt(x ** 2 + y ** 2)
    w = (1.0 / (h * np.sqrt(np.pi))) ** 3 * np.exp(-r ** 2 / h ** 2)
    return w


def grad_kernel(x, y):
    """
    Gradient of the Gausssian Smoothing kernel (2D)
    x, y - coordinates
    h - smoothing depth
    """

    r = np.sqrt(x ** 2 + y ** 2)
    n = -2 * np.exp(-r ** 2 / h ** 2) / h ** 5 / np.pi ** (3 / 2)
    wx = n * x
    wy = n * y

    return wx, wy


def relative_coordinates(r):
    """
    Returns coordinates of the j-th particle relative to the i-th one
    r - nx2 matrix
    """
    size = r.shape[0]
    rx = r[:, 0].reshape((size, 1))
    ry = r[:, 1].reshape((size, 1))

    dx = rx - rx.T
    dy = ry - ry.T

    return dx, dy


def density(r):
    """
    Returns density matrix at particle positions
    r - nx2 coordinate matrix
    """
    dx, dy = relative_coordinates(r)
    size = r.shape[0]
    rho = np.sum(m * kernel(dx, dy), 1).reshape((size, 1))

    return rho


def pressure(rho):
    """
    Returns pressure
    """
    p = k * rho ** (1 + 1 / power)

    return p


def acceleration(r, v):
    """
    Returns acceleration
    """
    rho = density(r)
    p = pressure(rho)
    dx, dy = relative_coordinates(r)
    d_wx, d_wy = grad_kernel(dx, dy)

    ax = -np.sum(m * (p / rho ** 2 + p.T / rho.T ** 2) * d_wx, 1)
    ay = -np.sum(m * (p / rho ** 2 + p.T / rho.T ** 2) * d_wy, 1)
    ay += g
    a = np.array([ax, ay])
    a = a.T
    a -= nu * v

    return a


def reflect(vx, vy, alpha):
    """
    Returns velocity components after the collision of the particle with a wall
    vx, vy - velocity coordinates
    alpha - angle from the center of the particle to the point of contact with the wall
    """

    u = vy * math.cos(alpha) - vx * math.sin(alpha)
    w = vx * math.cos(alpha) + vy * math.sin(alpha)

    elasticity = 1
    ux = -u * math.sin(alpha) - elasticity * w * math.cos(alpha)
    uy = u * math.cos(alpha) - elasticity * w * math.sin(alpha)

    return ux, uy


def make_water(left, right, up, down, number):
    """
    Creates water particles in given rectangle
    left, right, up, down - corresponding boundaries
    number - number of particles being created
    """
    x = np.random.randint(left, (right + left) / 2, number).astype(np.float64)
    y = np.random.randint((up + down) / 2, down, number).astype(np.float64)
    r = np.array([x, y]).T
    v = np.zeros(r.shape)

    return r, v


def step(r, v):
    """
    Returns r and v at time t+dt given r and v at time t
    """
    acc = acceleration(r, v)

    v += acc * dt
    r += v * dt

    return r, v
