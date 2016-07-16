#!/usr/bin/env python
import numpy as np

class NCPath:

	def __init__( self ):
		self.filename	= ""
		self.paths		= []		# Paths read from nc file

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
								s0[1] = float( y0[-1] )

						# Check for Z value
						elif ( t0 & 0b100 ):
							s0[0] = float( x0[-1].split("Z")[0] )
							s0[2] = float( z0[-1] )

						else: s0[0] = float(x0[-1])

					elif t0 & 0b010:
						# Check for Z Value
						if ( t0 & 0b100 ):
							s0[1] = float( y0[-1].split("Z")[0] )
							s0[2] = float( z0[-1] )
						else:
							s0[1] = float( y0[-1] )

					else:
						s0[2] = float( z0[-1].split("F")[0] )
			
					self.paths.append(s0)

		return 0


	def LoadFile( self, path ):
		file = open( path, 'rb' )
		lines = []
		for line in file:
			lines.append(line)

		return self.GetPaths(lines)


