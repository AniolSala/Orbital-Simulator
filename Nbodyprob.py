import numpy as np

# Pas de temps:
h = 400.0

# Number of bodys:
N = 3

# Vector with all positions and velocities:
y0 = np.zeros(4 * N)

# Interesting exercice: Look what happens when a body leaves
# the earth from its surface (earth radius = 0.06371) with a
# velocity equals to the velocity scape (vscape = 11.2e-5).

# Array with the initial conditions:
# y0 = [x1, ..., xN, y1, ..., yN, velx1, ..., velxN, vely1, ..., velyN].

# Intitial postions 'x' of the different bodies:
y0[0:N] = np.array([0, 0, -10], dtype=float)

# Intitial postions 'y' of the different bodies:
y0[N:2 * N] = np.array([0, -4, -10], dtype=float)

# Initial velocities in the x direction:
y0[2 * N:3 * N] = np.array([0, 10.23e-6, 5e-6], dtype=float)

# Initial velocities in the y direction:
y0[3 * N:] = np.array([0, 0, 0], dtype=float)   # , 0, 0, 0], dtype = float)

# Masses of all the bodies:
m = np.array([1.0, 0.0123, 0.01])  # , 2*0.0123, 2*0.0123, 10*0.0123])

# Physical constants of the system:
G = 4e-10


def derivates(t, y):
    '''
    Matrix with the distances rij and tensor of
    the unitary vectors [uij(x), uij(y)]:

    '''
    global G, m, N

    r = np.zeros((N, N))
    u = np.zeros((2, N, N))
    # Array to be returned:
    ynew = np.zeros(4 * N)

    # Principal loop:
    for row in range(N):
        for col in range(row + 1, N):

            r[row, col] = np.sqrt((y[col] - y[row])**2 +
                                  (y[col + N] - y[row + N])**2)
            u[:, row, col] = - 1 * np.array([y[col] - y[row], y[col + N] -
                                             y[row + N]]) / r[row, col]

    # We have to symmetrize the matrix with the distances of the particles.
    # To avoid the divideb by zero problem we make the diagonal of ones.
    r += r.T + np.eye(N)
    u[0] -= u[0].T  # Antisymmetrize the unitary vectors.
    u[1] -= u[1].T
    F = G * (1 / r**2 - np.eye(N)) * m
    dx = np.diagonal(np.dot(F, u[0]))
    dy = np.diagonal(np.dot(F, u[1]))

    ynew[:2 * N] = y[2 * N:]
    ynew[2 * N:3 * N] = dx
    ynew[3 * N:] = dy

    return ynew


def RK4(t, y):
    '''RK4 method. All the physics is in the function derivates'''
    global h

    k1 = derivates(t, y)
    k2 = derivates(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = derivates(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = derivates(t + h, y + h * k3)

    return y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
