import numpy as np

# Pas de temps:
h = 400.0

# Número de cossos (assumim que és moviment en 2D):
N = 2

# El vector posició del problema tindrà dimensió 4N:
y0 = np.zeros(4 * N)

# Exercici interessant: veure com queden o no atrapats dos planetes que
# surten de la superfície de la terra (rterra = 0.06371) en funció de
# la vel. inicial.
vscape = 11.2e-5

# Array amb les cond. inicials:
# y0 = [x1, ..., xN, y1, ..., yN, velx1, ..., velxN, vely1, ..., velyN].

# Posicions inicials x:
y0[0:N] = np.array([0, 0], dtype=float)

# Posicions inicials y:
y0[N:2 * N] = np.array([0, -4], dtype=float)  # , -5, -8, 8], dtype = float)

# Velocitats inicials x:
y0[2 * N:3 * N] = np.array([0, 10.23e-6], dtype=float)

# Velocitats inicials y:
y0[3 * N:] = np.array([0, 0], dtype=float)   # , 0, 0, 0], dtype = float)

# Entrem les masses en una array:
m = np.array([1.0, 0.0123])  # , 2*0.0123, 2*0.0123, 10*0.0123])

# Constants físiques del problema (les unitats són en 10^8m i les
# masses en relació a la de la terra):
# Nota: la distància terra-lluna amb aquestes unitats equival a 4.
G = 4e-10

# Aquí hi haurà la física del problema.


def derivates(t, y):
    '''
    Matriu amb les distancies rij i tensor dels vectors
    unitaris [uij(x), uij(y)]:
    '''
    global G, m, N

    r = np.zeros((N, N))
    u = np.zeros((2, N, N))
    # Tupla que es retornarà:
    ynew = np.zeros(4 * N)

    # Loop principal:
    for row in range(N):
        for col in range(row + 1, N):

            r[row, col] = np.sqrt((y[col] - y[row])**2 +
                                  (y[col + N] - y[row + N])**2)
            u[:, row, col] = - 1 * np.array([y[col] - y[row], y[col + N] -
                                             y[row + N]]) / r[row, col]

    # Simetritzem la matriu on hem col·locat les dist. entre partícules.
    # Per no tenir el probl. de dividir per zero fem la diagonal = 1.
    r += r.T + np.eye(N)
    u[0] -= u[0].T  # Antisimetritzem els vectors posició unitaris.
    u[1] -= u[1].T
    F = G * (1 / r**2 - np.eye(N)) * m
    dx = np.diagonal(np.dot(F, u[0]))
    dy = np.diagonal(np.dot(F, u[1]))

    ynew[:2 * N] = y[2 * N:]
    ynew[2 * N:3 * N] = dx
    ynew[3 * N:] = dy

    return ynew


def RK4(t, y):
    '''Aquí és on aniran les ks del mètode RK4'''
    global h

    k1 = derivates(t, y)
    k2 = derivates(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = derivates(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = derivates(t + h, y + h * k3)

    return y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
