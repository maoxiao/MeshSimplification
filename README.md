MeshSimplification
==============

Mesh Simplification algorithm by using vertex clustering

Requirements
----------
Python 2.7

OpenGL for program with UI

How to use
----------

###With UI
The "load" program (using OpenGL for rendering the model) of this version is complied on OS X 10.9. 

Please run the program on OS X operating system.

###No UI
Usage: **python main.py filename unit**

**"filename"** is any files in "original_mesh" folder

**"unit"** is the length of the bounding box of the model

for example: **python main.py cow.off 0.02**



Reference
---------

[Multi-Resolution 3D Approximations for Rendering Complex Scenes]
[Multi-Resolution 3D Approximations for Rendering Complex Scenes]: http://www.cs.uu.nl/docs/vakken/ddm/slides/papers/rossignac.pdf

[Model Simplification Using Vertex-Clustering  ]
[Model Simplification Using Vertex-Clustering  ]: http://www.comp.nus.edu.sg/~tants/Paper/simplify.pdf

