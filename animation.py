import pyglet
import pyglet.gl
from planet import Planet
from Nbodyprob import y0, RK4, h, N, m
import numpy as np


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.position = y0
        self.iterat = 0

        self.step = 0.
        self.planetlist = []
        for i in range(N):
            self.planetlist.append(
                Planet(self.position[i], self.position[i + N], m[i]))

    def on_draw(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

        # Drawing the planets
        for planet in self.planetlist:
            planet.vertices.draw(pyglet.gl.GL_POLYGON)

        self.fps_display.draw()
        self.fps_display.set_fps(50)

    def update(self, dt):
        for i in range(30):
            self.step += h
            y = RK4(self.step, self.position)
            self.position = y

        for i in range(N):
            self.planetlist[i].update(dt, np.array((y[i], y[i+N])))


if __name__ == '__main__':
    world = MyWindow(width=800, height=600)
    pyglet.gl.glClearColor(.1, .1, .1, .1)
    world.on_draw()

    pyglet.clock.schedule_interval(world.update, 1 / 60.)
    pyglet.app.run()