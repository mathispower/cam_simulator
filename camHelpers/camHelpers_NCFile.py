#!C:/Python27/python -u
import	numpy	  as	 np
from	pyglet.gl import *

class ncModel:

	def __init__( self, path ):
		self.extents	= { "xMin":0.0,
							"xMax":0.0,
							"yMin":0.0,
							"yMax":0.0,
							"zMin":0.0,
							"zMax":0.0,
							"xWidth":0.0,
							"yWidth":0.0,
							"zWidth":0.0 }
		self.filename	= path.split("/")[-1].split(".")[0]
		self.paths		= []		# Paths read from nc file
		self.LoadFile(path)

	def DrawModel(self, posM, rotM):
		""" This function loads the model for rendering.
			posM = [ position_X, position_Y, position_Z ]
			rotM = [ angle, axis_X_on/off, axis_Y_on/off, axisZ_on/off ]
		"""

		glPushMatrix()

		glTranslatef( posM[0], posM[1], posM[2] )
		glRotatef( rotM[0], rotM[1], rotM[2], rotM[3] )

		glColor3f( 0.0, 0.0, 1.0 )

		glBegin(GL_LINES)

		# Screen-Z is into the monitor but model-z is vertical
		for path in self.paths:
			x = path[0]
			y = path[2]
			z = path[1]
			glVertex3f( x, y, z )

		glEnd()

		glPopMatrix()

	def GetPaths( self, lines ):
		ind = 0
		for line in lines:
			line = line[:-2]
			if len( line.split(".") ) > 1:
				x0 = line.split("X")
				y0 = line.split("Y")
				z0 = line.split("Z")
				t0 = 0

				# Initialize
				if (len(x0)>1) or (len(y0)>1) or (len(z0)>1):
					s0 = [ 0.0, 0.0, 0.0 ]
					i = len(self.paths)

					if len( line.split("X") ) > 1: t0 += 0b001
					if len( line.split("Y") ) > 1: t0 += 0b010
					if len( line.split("Z") ) > 1: t0 += 0b100

					if t0 & 0b001:

						# Check for Y value
						if ( t0 & 0b010 ):
							s0[0] = float( x0[-1].split("Y")[0] )

							# Check for Z value
							if ( t0 & 0b100 ):
								t1 = y0[-1].split("Z")
								s0[1] = float( t1[0] )
								s0[2] = float( t1[-1] )
							else:
								print i
								if i > 0: s0[2] = self.paths[-1][2]
								s0[1] = float( y0[-1] )

						# Check for Z value
						elif ( t0 & 0b100 ):
							s0[0] = float( x0[-1].split("Z")[0] )
							s0[2] = float( z0[-1] )

							if i > 0: s0[1] = self.paths[-1][1]

						else:
							s0[0] = float(x0[-1])
							if i > 0:
								s0[1] = self.paths[-1][1]
								s0[2] = self.paths[-1][2]

					elif t0 & 0b010:
						# Check for Z Value
						if ( t0 & 0b100 ):
							s0[1] = float( y0[-1].split("Z")[0] )
							s0[2] = float( z0[-1] )
							if i > 0: s0[0] = self.paths[-1][0]
						else:
							s0[1] = float( y0[-1] )
							if i > 0:
								s0[0] = self.paths[-1][0]
								s0[2] = self.paths[-1][2]

					else:
						s0[2] = float( z0[-1].split("F")[0] )
						if i > 0:
							s0[0] = self.paths[-1][0]
							s0[1] = self.paths[-1][1]
			
					self.paths.append(s0)

					if s0[0] < self.extents["xMin"]: self.extents["xMin"] = s0[0]
					if s0[0] > self.extents["xMax"]: self.extents["xMax"] = s0[0]
					if s0[1] < self.extents["yMin"]: self.extents["yMin"] = s0[1]
					if s0[1] > self.extents["yMax"]: self.extents["yMax"] = s0[1]
					if s0[2] < self.extents["zMin"]: self.extents["zMin"] = s0[2]
					if s0[2] > self.extents["zMax"]: self.extents["zMax"] = s0[2]

		self.extents["xWidth"] = self.extents["xMax"] - self.extents["xMin"]
		self.extents["yWidth"] = self.extents["yMax"] - self.extents["yMin"]
		self.extents["zWidth"] = self.extents["zMax"] - self.extents["zMin"]

		return 0

	def LoadFile( self, path ):
		self.path = path
		file = open( self.path, 'rb' )
		lines = []
		for line in file:
			lines.append(line)

		return self.GetPaths(lines)

if __name__ == "__main__":
	# Get the nc file into the script
	DIR	 = "C:/Code/nc/"
	FILE = "base.nc"

	model = ncModel(DIR+FILE)

	index = 0
	for path in model.paths:
		if index < 10: print path
		index += 1

	print "\nThere were %d paths in the model." % index
