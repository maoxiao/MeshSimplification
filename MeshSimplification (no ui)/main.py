
# coding: utf-8 -*-

import os
from parser import Parser
from mesh import *
from simplification import Simplification

def createOutput(fname, simplifier, mesh):
    if not os.path.isdir("./output"):
        os.mkdir("./output")
    model_name = fname[:-4]
    if not os.path.isdir("./output/" + model_name):
        print fname[:-4]
        os.mkdir("./output/" + model_name)
    
    out_dir = "./output/" + model_name + "/"
    simplifier.generateFile(mesh, out_dir)
    
    return simplifier.output


if __name__ == '__main__':

    if len(sys.argv) < 3 or not os.path.isfile("./original_mesh/" + sys.argv[1]):
        print "Usage: python %s filename unit" % sys.argv[0]
        print "for example: python %s cow.off 0.02" % sys.argv[0]
        print "check original_mesh/ folder for mesh file"
        sys.exit(0)
    fname = sys.argv[1]
    try:
        unit  = float(sys.argv[2])
    except Exception as e:
        print "Usage: python %s filename unit" % sys.argv[0]
        print "for example: python %s cow.off 0.02" % sys.argv[0]
        print "check original_mesh/ folder for mesh file"
        sys.exit(0)

    mesh = Parser.load("./original_mesh/" + fname)
    simplifier = Simplification(mesh)
    simplified_mesh = simplifier.simplify(unit)
    output = createOutput(fname, simplifier, simplified_mesh)
    simplifier.printResult()
    
    