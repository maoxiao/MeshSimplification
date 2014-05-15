#-*- coding: utf-8 -*-

import sys
import os
import math

from mesh import *

class Parser(object):

    @staticmethod
    def load(fname):
        isExist = os.path.isfile(fname)
        if not isExist:
            print "File not found!"
            exit(0)
        print "loading " + fname + " ..."
        
        mesh = Mesh()
        mesh.filename = fname
        f = open(fname)
        lines = f.readlines()
        Parser.parse(lines, mesh)      
        f.close()
        print "Model loaded!"
        mesh.calNormals()
        return mesh
        
    @staticmethod
    def parse(lines, mesh):
        num = -1
#         global vertex_count, face_count, edge_count
#         global vertex_list, face_list, vertex_within_faces
       
        tmep_v = 0
        temp_f = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            #print "line num: " + str(i)
            if i == 0 and line.upper() != "OFF":
                print line
                print "Invalid file!"
                exit(0)
            else:
                if not line or i == 0 or line.startswith("#"):
                    continue  
                
                num += 1
                content = line.split()
                #get vertex_count , face_count , edge_count
                if num == 0:
                    mesh.vertex_count = int(content[0].strip())
                    mesh.face_count = int(content[1].strip())
                    mesh.edge_count = int(content[2].strip())
                    #print vertex_count , face_count , edge_count
                    tmep_v = mesh.vertex_count
                    temp_f = mesh.face_count
                    
                else:
                    #get vertex coordinate
                    if tmep_v > 0:
                        tmep_v = tmep_v - 1
                        x = float(content[0].strip())
                        y = float(content[1].strip())
                        z = float(content[2].strip())
                        vertex = Vertex([x, y, z])
                        mesh.vertex_list.append(vertex)
                        mesh.getBoundingBox(x, y, z)
                        
                        
                    #get vertex indices of each face   
                    elif temp_f > 0:
                        temp_f = temp_f - 1
                        v_num = int(content[0])
                        #print "test " + str([int(e.strip()) for e in content[1:int(content[0])]]) 
                        vertex_indices = [int(e.strip()) for e in content[1:v_num+1]]
                        
                        prev = -1
                        temp = -1
                        #get vertex_within_faces
                        for j, index in enumerate(vertex_indices):
#                             if not vertex_within_faces.has_key(index):
#                                 vertex_within_faces[index] = []
#                             vertex_within_faces[index].append(len(face_list))
                            temp = temp + 1
#                             print "temp: " + str(temp) + " " + str(index+1) + " " + str(vertex_indices) 
                            v = mesh.vertex_list[index]
                            v.faces.append(len(mesh.face_list))
#                             if prev > -1:
# #                                 mesh.vertex_list[index-1].faces.append(len(mesh.face_list))
# #                                 coordinate = mesh.vertex_list[index-1].coordinate
# #                                 mesh.vertex_list[index-1].addEdge(index, coordinate)
#                                 v1 = mesh.vertex_list[index-1]
#                                 v.addEdge(index, v1.coordinate)
#                                  
# #                             mesh.vertex_list[index].faces.append(len(mesh.face_list))
# #                             coordinate = mesh.vertex_list[index].coordinate
# #                             mesh.vertex_list[index].addEdge(index, coordinate)
#                             if prev != vertex_indices[-1]:
#                                 v2 = mesh.vertex_list[index+1]
#                                 v.addEdge(index, v2.coordinate)
#                         
#                             prev = index
                            v1 = v2 = None
                            if j > 0:
                                #v1 = mesh.vertex_list[j-1]
                                v1 = mesh.vertex_list[vertex_indices[j-1]]
                                v.addEdge(vertex_indices[j-1], v1.coordinate)
#                                 if index == 0:
#                                     print "v1: ", v1.coordinate
#                                     print "edges: ", mesh.vertex_list[0].edges, "vector: ", mesh.vertex_list[0].edge_vectors
                            if j < v_num - 1:
                                #v2 = mesh.vertex_list[j+1]
                                v2 = mesh.vertex_list[vertex_indices[j+1]]
                                v.addEdge(vertex_indices[j+1], v2.coordinate)
#                                 if index == 0:
#                                     print "v2: ", v2.coordinate
#                                     print "edges: ", mesh.vertex_list[0].edges, "vector: ", mesh.vertex_list[0].edge_vectors
                           
#                             prev = index
#                         if index == 0:
#                             print "edges: ", mesh.vertex_list[0].edges, "vector: ", mesh.vertex_list[0].edge_vectors
                           
                        
                        mesh.face_list.append(Face(vertex_indices))
                        
# mesh = Parser.load("cube.off")
# 
# for i, v in enumerate(mesh.vertex_list):
#     print i, ": ",v.edges


