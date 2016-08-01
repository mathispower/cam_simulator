#!C:/Python27/python -u
import numpy as np
import	pyglet
from	pyglet.gl		import *
from	pyglet.window	import key,mouse
import	sys

class window(pyglet.window.Window):

	def __init__(self):
		self.alive = True

		self.models = []

		# Setup the OpenGL window
		self.winWidth  = 800
		self.winHeight = 600
		self.title	   = "CAM Simulator"

		self.views = { "ISO":  [ 6, 6, 6, 0, 0, 0, 0, 1, 0 ],
					   "Top":  [ 0, 6, 0, 0, 0, 0, 0, 0, -1],
					   "Front":[ 0, 0, 6, 0, 0, 0, 0, 1, 0 ],
					   "Right":[ 6, 0, 0, 0, 0, 0, 0, 1, 0 ],
					 }

		self.curView = "Top"

		self.lookS = self.views[self.curView]

		try:
			# Try and create a window with multisampling (antialiasing)
			config = Config( sample_buffers=1,
							 samples=4, 
							 depth_size=16,
							 double_buffer=True, )

			super(window, self).__init__( self.winWidth,
										  self.winHeight,
										  self.title,
										  resizable=True,
										  config=config )

		except pyglet.window.NoSuchConfigException:
			print "Unable to use antialiasing."; sys.stdout.flush()
			# Fall back to no multisampling for old hardware
			super(window, self).__init__( self.winWidth,
										  self.winHeight,
										  self.title,
										  resizable=True )

		super(window, self).set_location(0,30)

		self.init()

	def on_close(self):
		self.alive = False

	def on_draw(self):
		self.render()

	def init(self):

		self.fps_display = pyglet.window.FPSDisplay(self)

		# One-time GL setup
		# glClearColor(0, 0, 0, 1)
		# glColor3f(1, 0, 0)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)

		# Uncomment this line for a wireframe view
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

		# Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
		# but this is not the case on Linux or Mac, so remember to always 
		# include it.
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glEnable(GL_LIGHT1)

		# Define a simple function to create ctypes arrays of floats:
		def vec(*args):
		    return (GLfloat * len(args))(*args)

		glLightfv(GL_LIGHT0, GL_POSITION, vec(10, 10, 1, 0))
		glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
		glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
		glLightfv(GL_LIGHT1, GL_POSITION, vec(10, 0, 15, 0))
		glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
		glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

		# Enable to keep the vertex set colors while using lights
		glEnable(GL_COLOR_MATERIAL)

		glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(1.0, 1.0, 1.0, 1))
		glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
		glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho( -10, self.winWidth+10, -10, self.winHeight+10, 0.1, 10000 )
		# gluPerspective(70., self.winWidth / float(self.winHeight), .1, 1000.)

	def on_key_press(self, symbol, modifiers):
		increment = 1
		if   symbol == key.DOWN:
			self.lookS[1] -= increment
			self.lookS[4] -= increment

		elif symbol == key.UP:
			self.lookS[1] += increment
			self.lookS[4] += increment

		elif symbol == key.LEFT:
			self.lookS[0] -= increment
			self.lookS[3] -= increment

		elif symbol == key.RIGHT:
			self.lookS[0] += increment
			self.lookS[3] += increment

		elif symbol == key.PAGEUP:
			self.lookS[2] -= increment
			self.lookS[5] -= increment

		elif symbol == key.PAGEDOWN:
			self.lookS[2] += increment
			self.lookS[5] += increment

		elif symbol == key._0:
			self.curView = "ISO"
			self.lookS = self.views[self.curView]

		elif symbol == key._1:
			self.curView = "Front"
			self.lookS = self.views[self.curView]

		elif symbol == key._2:
			self.curView = "Top"
			self.lookS = self.views[self.curView]

		elif symbol == key._3:
			self.curView = "Right"
			self.lookS = self.views[self.curView]

		# elif symbol == key.A:
		# 	mRotX = 0.0

		# elif symbol == key.Q:
		# 	mRotX = 1.0

		# elif symbol == key.W:
		# 	mRotY = 1.0

		# elif symbol == key.S:
		# 	mRotY = 0.0

		# elif symbol == key.D:
		# 	mRotZ = 0.0

		# elif symbol == key.E:
		# 	mRotZ = 1.0

		elif symbol == key.X:
			sys.exit(0)

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == mouse.LEFT:
			pass
		elif button == mouse.RIGHT:
			t0 = dy/float(self.winHeight)*10

			# Normalize view vector
			t1 = self.lookS[0] - self.lookS[3]
			t2 = self.lookS[1] - self.lookS[4]
			t3 = self.lookS[2] - self.lookS[5]

			mag = np.sqrt( np.power(t1, 2) + np.power(t2, 2) + np.power(t3, 2) )

			norm = [t1/mag, t2/mag, t3/mag]

			# Move view camera along view vector
			for i in range(3): self.lookS[i] -= norm[i] * t0

	def on_mouse_motion(self, x, y, dx, dy):
		pass

	def on_mouse_press(self, x, y, button, modifiers):
		if button == mouse.LEFT:
			# Get the view vector
			vv = [ self.lookS[0] - self.lookS[3],
				   self.lookS[1] - self.lookS[4],
				   self.lookS[2] - self.lookS[5] ]

			# Offset vector (Shift on plane normal to view vector)
			

			# Calculate new position in world space


		elif button == mouse.RIGHT:
			pass

	def on_mouse_release(self, x, y, button, modifiers):
		if button == mouse.LEFT:
			pass
		elif button == mouse.RIGHT:
			pass

	def render(self):
		glClearColor(0.5, 0.5, 0.5, 1)

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		self.fps_display.draw()

		# glOrtho(0, winWidth, 0, winHeight, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()



		gluLookAt( *self.lookS )

		

		# Draw all of the models attached to this instance
		for model in self.models: model[0](model[1],model[2])

		self.flip()

	def on_resize(self, width, height):
		""" Override the default on_resize handler to create a 3D projection. """
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(70., width / float(height), .1, 1000.)
		glMatrixMode(GL_MODELVIEW)
		return pyglet.event.EVENT_HANDLED

	def run(self):
		while self.alive:
			event = self.dispatch_events()
			self.render()

if __name__ == "__main__":
	from camHelpers_NCFile import ncModel

	ncDIR  = "C:/Code/nc/"
	ncFILE = "base.nc"
	ncModel = ncModel(ncDIR+ncFILE)

	mPosX = -2.0; mPosY =  0.0; mPosZ = -2.0
	mRotX =  1.0; mRotY =  0.0; mRotZ =  0.0
	angle = 20.0;
	label_1 = "[0,0,0,0]"

	win = window()

	win.run()
