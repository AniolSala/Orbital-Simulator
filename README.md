# Orbital-Simulator
A planets orbital simulator using python and pyglet. The gravitational equations are solved using the Runge-Kutta method.

# The units are the following:
Unit of distance: 10e8 m (hence the distance between the Earth and the Moon is 4).
Unit of velocity: 10e-8 m/s.
Unit of time: 1s
Unit of mass: Mass of the Earth

For example, to simulate the Earth-Moon system, you should use N = 2 and:

y0[0:N] = np.array([0, 0], dtype=float)

y0[N:2 * N] = np.array([0, -4], dtype=float)  # , -5, -8, 8], dtype = float)

y0[2 * N:3 * N] = np.array([0, 10.23e-6], dtype=float)

y0[3 * N:] = np.array([0, 0], dtype=float)   # , 0, 0, 0], dtype = float)

You can set N = 3 and have fun throwing meteorites.
