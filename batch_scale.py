#!/usr/bin/python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE":
# <pieis2pi@u.washington.edu> wrote this file.  As long as you retain this
# notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy me a beer in return.
# -Evan Thomas
# ----------------------------------------------------------------------------

import glob
import numpy as np
from stl import mesh

firstoctant = True
scale = 0.5
directory = "."
for filename in glob.glob(directory+"/*.stl"):
	stlmesh = mesh.Mesh.from_file(filename)
	if(firstoctant):
		minpoint = [0]*3
		for i in [0,1,2]:
			minpoint[i]=min(min(stlmesh.v0[:,i]),
							min(stlmesh.v1[:,i]),
							min(stlmesh.v2[:,i]))
		stlmesh.v0-=minpoint
		stlmesh.v1-=minpoint
		stlmesh.v2-=minpoint
	stlmesh.points*=scale
	stlmesh.save(filename.rstrip("stl")+"scaled.stl")
