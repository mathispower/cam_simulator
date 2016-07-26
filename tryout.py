#!/usr/bin/env python
import	numpy as np
import	pyglet
from	pyglet.gl		import *
from	pyglet.window	import key,mouse
from	stl				import mesh
import	sys
sys.path.append("camHelpers")
import camHelpers as myH

# Get the nc file into the script
DIR	 = "C:/Code/nc/"
FILE = "base.nc"

# Grab STL model
DIR2	 = "C:/Code/nc/"
FILE2 = "Base.stl"
# mesh = mesh.Mesh.from_file(DIR+FILE)

label_1 = "[0,0,0,0]"

# Setup model parameters
mPosX = -2.0; mPosY =  0.0; mPosZ = -2.0
mRotX =  1.0; mRotY =  0.0; mRotZ =  0.0
angle = 20.0;

fps_display = pyglet.clock.ClockDisplay()

#### SETUP
# Setup the OpenGL window
winWidth  = 800
winHeight = 600

try:
	# Try and create a window with multisampling (antialiasing)
	config = Config( sample_buffers=1,
					 samples=4, 
					 depth_size=16,
					 double_buffer=True, )

	window = pyglet.window.Window(	winWidth,
									winHeight,
									"CAM Simulator",
									resizable=True,
									config=config )

except pyglet.window.NoSuchConfigException:
	print "Unable to use antialiasing."; sys.stdout.flush()
	# Fall back to no multisampling for old hardware
	window = pyglet.window.Window(	winWidth,
									winHeight,
									"CAM Simulator",
									resizable=True )
#### END SETUP

def Model_GroundPlane():
	glPushMatrix()

	glTranslatef( 0, -10, 0 )

	glColor3f( 0.0, 1.0, 0.0 )

	glBegin( GL_QUADS );

	glVertex3f( -20.0, 0.0, -100.0 )
	glVertex3f( -20.0, 0.0,  100.0 )
	glVertex3f(  20.0, 0.0,  100.0 )
	glVertex3f(  20.0, 0.0, -100.0 )

	glEnd();

	glPopMatrix()

def Model_STL():
	return 0

def setup():
	# One-time GL setup
	# glClearColor(0, 0, 0, 1)
	# glColor3f(1, 0, 0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_CULL_FACE)

	# Uncomment this line for a wireframe view
	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	# Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
	# but this is not the case on Linux or Mac, so remember to always 
	# include it.
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHT1)

	# Define a simple function to create ctypes arrays of floats:
	def vec(*args):
	    return (GLfloat * len(args))(*args)

	glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
	glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
	glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
	glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
	glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

	# Enable to keep the vertex set colors while using lights
	glEnable(GL_COLOR_MATERIAL)

	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(1.0, 1.0, 1.0, 1))
	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
	glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(70., winWidth / float(winHeight), .1, 1000.)

@window.event
def on_draw():
	glClearColor(0.5, 0.75, 0.5, 1)

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	# glOrtho(0, winWidth, 0, winHeight, -1, 1)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	fps_display.draw()

	Model_GroundPlane()

	ncModel.DrawModel( [mPosX,mPosY,mPosZ], [angle,mRotX,mRotY,mRotZ] )

	# label = pyglet.text.Label( label_1,
	# 						   font_size=112,
	# 						   x=winWidth//2, y=winHeight//2,
	# 						   anchor_x='center', anchor_y='center',
	# 						   color=(255, 255, 255, 255),)
	# 						   # batch=tBatch)
	# label.draw()

	# tBatch.draw()


@window.event
def on_key_press(symbol, modifiers):
	global mPosX, mPosY, mPosZ, mRotX, mRotY, mRotZ, angle
	global label_1
	if   symbol == key.DOWN:
		mPosY = mPosY - 1

	elif symbol == key.LEFT:
		mPosX = mPosX - 1

	elif symbol == key.RIGHT:
		mPosX = mPosX + 1

	elif symbol == key.UP:
		mPosY = mPosY + 1

	elif symbol == key.PAGEUP:
		mPosZ = mPosZ + 1

	elif symbol == key.PAGEDOWN:
		mPosZ = mPosZ - 1

	elif symbol == key._1:
		angle -= 10.0

	elif symbol == key._2:
		angle += 10.0

	elif symbol == key.A:
		mRotX = 0.0

	elif symbol == key.Q:
		mRotX = 1.0

	elif symbol == key.W:
		mRotY = 1.0

	elif symbol == key.S:
		mRotY = 0.0

	elif symbol == key.D:
		mRotZ = 0.0

	elif symbol == key.E:
		mRotZ = 1.0

	elif symbol == key.X:
		sys.exit(0)

	label_1  = "[ %.0f, %.0f, %.0f ]\t" % (mPosX, mPosY, mPosZ)
	label_1 += "[ %.2f, %.0f, %.0f, %.0f ]" % (angle, mRotX, mRotY, mRotZ)
	print label_1; sys.stdout.flush()

@window.event
def on_mouse_press(x, y, button, modifiers):
	global mPosX, mPosY, mPosZ, mRotX, mRotY, mRotZ
	if   button == mouse.LEFT:
		pass
	elif button == mouse.RIGHT:
		pass
		# mPosX = mPosX - winWidth / float(2) + x
		# mPosY = mPosY - winHeight / float(2) + y

# @window.event
# def on_resize(winWidth,winHeight):
# 	glViewport(0,0, winWidth, winHeight)
# 	glMatrixMode(GL_PROJECTION)
# 	glLoadIdentity()
# 	glOrtho(0, winWidth, 0, winHeight, -1, 1)
# 	glMatrixMode(GL_MODELVIEW)

@window.event
def on_resize(width, height):
	# Override the default on_resize handler to create a 3D projection
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(70., width / float(height), .1, 1000.)
	glMatrixMode(GL_MODELVIEW)
	return pyglet.event.EVENT_HANDLED

if __name__ == "__main__":
	ncModel = myH.ncModel(DIR+FILE)

	setup()
	# tBatch = pyglet.graphics.Batch()

	pyglet.app.run()