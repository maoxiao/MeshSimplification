#-*- coding: utf-8 -*-

                       
import sys
import math

class Vertex(object):
    def __init__(self, coordinate=[],index=-1):
        self.coordinate = coordinate
        self.edges = set()
        self.faces = []
        self.remain_edges = []
        self.vertex_normal = []
        self.weight = sys.float_info.min
        self.edge_vectors = []
        #cell cell_index
        self.cell_index = -1
        
    def __repr__(self):
        return str(self.coordinate)
    
    def __str__(self):
        return self.__repr__()
    
    def addEdge(self, index, coordinate):
#         self.edges.append(vertex)
        if index not in self.edges:
            self.edges.add(index)
            self.edge_vectors.append(self.getEdgeVector(coordinate))
        
    def getEdgeVector(self, coordinate):
        return [coordinate[0]-self.coordinate[0], coordinate[1]-self.coordinate[1], coordinate[2]-self.coordinate[2]]


class Face(object):
    def __init__(self, vertex_indices=[]):
        self.vertex_indices = vertex_indices
        self.face_normal = []
    
    def __hash__(self):
        return hash(tuple(sorted(self.vertex_indices)))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return str(sorted(self.vertex_indices))
        
        
class Mesh(object):
    def __init__(self):
        self.filename = None
        self.face_count = 0
        self.vertex_count = 0
        self.edge_count = 0
        self.vertex_list = []
        self.face_list = []
        self.edge_list = {} #used for detecting holes
        self.minX = self.minY = self.minZ = sys.float_info.max
        self.maxX = self.maxY = self.maxZ = sys.float_info.min
        
    def updateBoundingBox(self):
        for v in self.vertex_list:
            self.getBoundingBox(v.coordinate[0], v.coordinate[1], v.coordinate[2])
        
    def getBoundingBox(self, x, y, z):
        if self.minX > x:
            self.minX = x
        if self.maxX < x: 
            self.maxX = x
        
        if self.minY > y:
            self.minY = y
        if self.maxY < y:
            self.maxY = y
    
        if self.minZ > z:
            self.minZ = z
        if self.maxZ < z:
            self.maxZ = z 
    
    @staticmethod          
    def crossProduct(p, q, r):
        a = [0] * 3
        b = [0] * 3
        d = [0] * 3
         
        a[0] = q[0] - p[0]
        a[1] = q[1] - p[1]
        a[2] = q[2] - p[2]
         
        b[0] = r[0] - p[0]
        b[1] = r[1] - p[1]
        b[2] = r[2] - p[2]
         
        d[0] = a[1] * b[2] - a[2] * b[1]
        d[1] = a[2] * b[0] - a[0] * b[2]
        d[2] = a[0] * b[1] - a[1] * b[0]
        
        return d
    
    @staticmethod
    def normalize(v):
        length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
 
        v[0] = v[0] / length
        v[1] = v[1] / length
        v[2] = v[2] / length
    
    def calNormals(self):
        for i in xrange(self.face_count):
            vertices =  self.face_list[i].vertex_indices

            self.face_list[i].face_normal = Mesh.crossProduct(self.vertex_list[vertices[0]].coordinate, self.vertex_list[vertices[1]].coordinate,
                                                              self. vertex_list[vertices[2]].coordinate)
            try:
                Mesh.normalize(self.face_list[i].face_normal)
            except Exception as e:
                print "length0: ",self.face_list[i]
                sys.exit(1)
        
        for i in xrange(self.vertex_count): 
            x = y = z = 0
            faces = self.vertex_list[i].faces
            num = len(faces)
            
            if num < 1:
                continue
            
            for index in faces:
                face = self.face_list[index]
                x = x + face.face_normal[0]
                y = y + face.face_normal[1]
                z = z + face.face_normal[2]
                
            self.vertex_list[i].vertex_normal = [x / num, y / num, z / num]
                
