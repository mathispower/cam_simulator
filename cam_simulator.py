#!/usr/bin/env python
import pyglet


window = pyglet.window.Window( 800, 600, "CAM Simulator" )

@window.event
def on_draw():
	window.clear()

pyglet.app.run()

