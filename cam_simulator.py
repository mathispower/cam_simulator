#!/usr/bin/env python
import	numpy as np
from	pyglet.gl		import *
import	sys
sys.path.append("camHelpers")
import camHelpers as cH

mainWin = cH.window()

# Get the nc file into the script
ncDIR	= "C:/Code/nc/"
ncFILE	= "base.nc"
ncModel = cH.ncModel( ncDIR + ncFILE )
ncPos	= [ 0.0, 0.0, 0.0 ]
ncRot	= [ 0.0, 0.0, 0.0 ]

# Grab STL model
stlDIR	= "C:/Code/nc/"
stlFILE = "Base.stl"
stlModel = cH.stlModel( stlDIR + stlFILE )
stlPos	= [ 0.0, 0.0, -stlModel.extents["zWidth"] ]
stlRot	= [ 0.0, 0.0, 0.0 ]


spherePos = [ 0.0, 0.0, 0.0]
sphereRot = [ 0.0, 0.0, 0.0]

label_1 = "[0,0,0,0]"

# Align the NC to the STL
# TODO
stlRot = [ -90.0, 0.0, 90.0 ]
ncRot  = [ -90.0, 0.0, 180.0 ]

def DrawSphere(pos,rot):
	glColor3f(0.0, 0.0, 1.0)
	glTranslatef( pos[0], pos[1], pos[2])
	gluSphere( gluNewQuadric(), 0.1, 10, 10 )

mainWin.models.append([ DrawSphere, spherePos, sphereRot ])

mainWin.models.append([ ncModel.DrawModel, ncPos, ncRot ])

mainWin.models.append([ stlModel.DrawModel, stlPos, stlRot ])

# sys.stdout.flush()

mainWin.run()



