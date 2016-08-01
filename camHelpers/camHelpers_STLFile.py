#!C:/Python27/python -u
#!C:/Python27/python -u
import	numpy	  as	 np
from	pyglet.gl import *
from	stl				import mesh

class stlModel:

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

		self.mesh = mesh.Mesh.from_file(path)

		self.Grab_Extents()

	def DrawModel(self, posM, rotM):
		""" This function loads the model for rendering.
			posM = [ position_X, position_Y, position_Z ]
			rotM = [ angle, axis_X_on/off, axis_Y_on/off, axisZ_on/off ]
		"""

		glPushMatrix()
		
		glRotatef( rotM[0], 1, 0, 0 )
		glRotatef( rotM[1], 0, 1, 0 )
		glRotatef( rotM[2], 0, 0, 1 )

		glTranslatef( posM[0], posM[1], posM[2] )

		glColor3f( 0.8, 0.8, 0.0 )

		glBegin(GL_TRIANGLES)

		# Screen-Z is into the monitor but model-z is vertical
		for vector in self.mesh.vectors:
			glVertex3f( vector[0,0], vector[0,1], vector[0,2] )
			glVertex3f( vector[1,0], vector[1,1], vector[1,2] )
			glVertex3f( vector[2,0], vector[2,1], vector[2,2] )

		glEnd()

		glPopMatrix()

	def Grab_Extents(self):
		r0 = [  1e9 ] * 3 # minimums
		r1 = [ -1e9 ] * 3 # maximums
		for point in self.mesh.points:
			for i in range(3):
				if point[i] < r0[i]: r0[i] = point[i]
				if point[i] > r1[i]: r1[i] = point[i]

		self.extents["xMin"] = r0[0]
		self.extents["xMax"] = r1[0]
		self.extents["yMin"] = r0[1]
		self.extents["yMax"] = r1[1]
		self.extents["zMin"] = r0[2]
		self.extents["zMax"] = r1[2]
		self.extents["xWidth"] = r1[0] - r0[0]
		self.extents["yWidth"] = r1[1] - r0[1]
		self.extents["zWidth"] = r1[2] - r0[2]

if __name__ == "__main__":
	stlDIR	= "C:/Code/nc/"
	stlFILE = "Base.stl"
	stlModel = stlModel( stlDIR + stlFILE )

	print stlModel.mesh.vectors