import pyglet
from numpy import array, pi, linspace, sin, cos
from Nbodyprob import RK4


class Planet():

    def __init__(self, x, y, m, color=[0, 255, 220, .7], scale=20):
        self.pos = array((x, y)) * scale
        self.m = m
        self.r = scale * (m**(1. / 3.))
        self.scale = scale

        N = 30
        self.clist = color * N
        self.vlist = []
        for angle in linspace(0, 2 * pi, N):
            self.vlist.append(self.r * cos(angle) + self.pos[0] + 400)
            self.vlist.append(self.r * sin(angle) + self.pos[1] + 400)

        self.vertices = pyglet.graphics.vertex_list(N, ('v2f', self.vlist),
                                                    ('c4f', self.clist))


    def update(self, dt, newpos):
        increment = newpos * self.scale - self.pos
        for i in range(len(self.vlist)):
            self.vlist[i] += increment[i % 2]
        for i in range(len(self.vertices.vertices)):
            self.vertices.vertices[i] = self.vlist[i]
        self.pos = newpos * self.scale
