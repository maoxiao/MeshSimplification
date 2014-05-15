#-*- coding: utf-8 -*-


import math
from mesh import *
from parser import Parser
import sys

class Simplification():
    def __init__(self, mesh):
        self.cell_table = {}
        self.original_mesh = mesh
        self.simplified_mesh = Mesh()
        self.simplified_mesh.filename = mesh.filename
        self.cell_list = []
        self.unit = 0
        self.output = ""

    def simplify(self, unit):
        self.unit = unit
        self.grade()
        self.subdivide()
        self.synthesize()
        self.triangulate()
        
        self.simplified_mesh.face_count = len(self.simplified_mesh.face_list)
        self.simplified_mesh.vertex_count = len(self.simplified_mesh.vertex_list)

        return self.simplified_mesh
    
    def printResult(self):
        print "[orginal]    face: ", self.original_mesh.face_count, "vertex: ", self.original_mesh.vertex_count
        print "[simplified] face: ", self.simplified_mesh.face_count, "vertex: ", self.simplified_mesh.vertex_count

    def subdivide(self):
        cell = None
        for vertex in self.original_mesh.vertex_list:

            cell_coordinate = self.getCell(vertex)
            
            if not self.cell_table.has_key(cell_coordinate):
                cell = Cell()
                cell.cell_index = len(self.cell_list)
                self.cell_table[cell_coordinate] = cell
                self.cell_list.append(cell)

            cell = self.cell_table[cell_coordinate]
            vertex.cell_index = cell.cell_index
            cell.vertices.append(vertex)
            
        self.connectCell()
            
    def connectCell(self):
        for cell in self.cell_list:
            for vertex in cell.vertices:
                for edge_index in vertex.edges:
                    index = self.original_mesh.vertex_list[edge_index].cell_index
                    if index not in cell.connected_cell and index != cell.cell_index:
                        cell.connected_cell.append(index)

    def synthesize(self):
        vertex_list = self.simplified_mesh.vertex_list
        for cell in self.cell_list:
            vertex = Vertex(self.synthesize_cell(cell))
            vertex.edges = set(cell.connected_cell)
            vertex_list.append(vertex)
            
    def synthesize_cell(self, cell):    
        x = y = z = 0
        weight_sum = 0
        if len(cell.vertices) < 2:
            return cell.vertices[0].coordinate
        
        for vertex in cell.vertices:
            weight = vertex.weight
            x = x + weight * vertex.coordinate[0]
            y = y + weight * vertex.coordinate[1]
            z = z + weight * vertex.coordinate[2]
            weight_sum = weight_sum + weight

        return [x/weight_sum, y/weight_sum, z/weight_sum]
            
        
    def getCell(self, vertex):
        x = self.original_mesh.minX
        y = self.original_mesh.minY
        z = self.original_mesh.minZ

        x_len = vertex.coordinate[0] - x
        y_len = vertex.coordinate[1] - y
        z_len = vertex.coordinate[2] - z
        
        mesh = self.original_mesh
        unit = self.unit * max([mesh.maxX - mesh.minX, mesh.maxY - mesh.minY, mesh.maxZ - mesh.minZ])
        
        x_component = x + unit * int(math.floor(x_len / unit))
        y_component = y + unit * int(math.floor(y_len / unit))
        z_component = z + unit * int(math.floor(z_len / unit))
        
        return (round(x_component, 10), round(y_component, 10), round(z_component, 10))
        
    def grade(self):
        for vertex in self.original_mesh.vertex_list:
            vertex.weight = self.calAngle(vertex) * len(vertex.faces)
    
    def calAngle(self, vertex):
        value = -100
        count = len(vertex.edges)
        edges = vertex.edge_vectors
        for i in xrange(count-1):
            for j in xrange(i+1, count):
                v = self.getCosTheta(edges[i], edges[j])
                if abs(v) > 1:
                    v = int(v)
                temp = math.acos(v)
                
                if temp > value:
                    value = temp
                    
        return 1 / value
    
    def getVectorLength(self, vector):
        return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
        
    def dotProduct(self, a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    
    def getCosTheta(self, a, b):
        return self.dotProduct(a, b) / (self.getVectorLength(a) * self.getVectorLength(b))
        
    def crossProduct(self, a, b):
        c = [0] * 3
        c[0] = a[1] * b[2] - a[2] * b[1]
        c[1] = a[2] * b[0] - a[0] * b[2]
        c[2] = a[0] * b[1] - a[1] * b[0]
        return c
            
    def checkFace(self, vertex_indices):
        for i, index1 in enumerate(vertex_indices):
            for j, index2 in enumerate(vertex_indices):
                if i != j and index1 == index2:
                    return False
        return True
    
    def triangulate(self):
        face_set = set()
        origina_vertex_list = self.original_mesh.vertex_list
        simplified_vertex_list = self.simplified_mesh.vertex_list
        
        for face in self.original_mesh.face_list:
            vertex_indices = face.vertex_indices
            
            new_vertex_indices = [origina_vertex_list[v].cell_index for v in vertex_indices]
            newFace = Face(new_vertex_indices) 
           
            if self.checkFace(new_vertex_indices) and newFace not in face_set:
                face_set.add(newFace)
                face_index = len(self.simplified_mesh.face_list)
                for vertex_index in new_vertex_indices:
                    simplified_vertex_list[vertex_index].faces.append(face_index)
                self.simplified_mesh.face_list.append(newFace)
                
        
    #off format
    def generateFile(self, mesh, out_dir):
        fname = out_dir + (mesh.filename.split("/")[-1])[:-4] + "_simplified_unit_" + str(self.unit) + ".off"
        self.output = fname
        print "generating ", fname
        f = open(fname, "w")
        f.write("OFF\n")
        #vertex_count , face_count , edge_count
        f.write(str(mesh.vertex_count) + " " + str(mesh.face_count) + " " + str(mesh.edge_count) + "\n")
        
        for vertex in mesh.vertex_list:
            coordinate = vertex.coordinate
            f.write(str(coordinate[0]) + " " + str(coordinate[1]) + " " + str(coordinate[2]) + "\n")
        for face in mesh.face_list:
            vertex_indices = face.vertex_indices
            size = len(vertex_indices)
            f.write(str(size))
            for vertex_index in vertex_indices:
                f.write(" " + str(vertex_index))
            f.write("\n")
        f.close()
    
    
class Cell():
    def __init__(self):
        self.cell_index = -1
        self.connected_cell = [] #connected cell indices
        self.vertices = []
        

