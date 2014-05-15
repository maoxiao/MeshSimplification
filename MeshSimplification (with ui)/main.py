 
# coding: utf-8 -*-

from Tkinter import *
import atexit
import os
from subprocess import Popen
import tkMessageBox

from parser import Parser
from mesh import *
from simplification import Simplification
 
 
from sys import platform as _platform

# OS X
if _platform == "darwin":
    load = "./load "
    
# Windows
elif _platform == "win32":
    load = "./load.exe "

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
 
class Window:
    def __init__(self, parent):
        self.mesh_list = ["cow.off", "bunny.off", "dragon.off"]
        self.parent = parent 
        self.selected_index = -1
        self.old_index = -1
        self.original_process = None
        self.simplified_process = None
        self.screen_width, self.screen_height = self.getScreenSize()
        self.var = IntVar()
        self.simplifier = None
        
        self.original_face_count_num = StringVar()
        self.original_vertex_count_num = StringVar()
        self.simplified_face_count_num = StringVar()
        self.simplified_vertex_count_num = StringVar()
        
        self.input_text = None
        
        self.setupWidgets()
        self.window_size = (360, 400)
        x_pos = (self.screen_width - self.window_size[0]) / 2 
        y_pos = (self.screen_height - self.window_size[1]) / 2 
        self.pos = (x_pos, y_pos)
        result = str(self.window_size[0]) + "x" + str(self.window_size[1]) + "+" + str(x_pos) + "+" + str(y_pos)
        self.parent.geometry(result)
        self.parent.title("Mesh Simplification Using Vertex Clustering")
        
    def setupWidgets(self):
        
        mesh_group = LabelFrame(self.parent, text="Mesh Files", padx=5, pady=5)
        
        mesh_group.pack(padx=10, pady=5)
        current_row = 0

        current_row = current_row + 1
        Radiobutton(mesh_group, text="cow.off", variable=self.var, value=1,
                      command=self.select).grid(row=current_row, sticky=W, columnspan=2)
        current_row = current_row + 1             

        Radiobutton(mesh_group, text="bunny.off", variable=self.var, value=2,
                      command=self.select).grid(row=current_row, sticky=W, columnspan=2)
        current_row = current_row + 1
        Radiobutton(mesh_group, text="dragon.off", variable=self.var, value=3,
                      command=self.select).grid(row=current_row, sticky=W, columnspan=2)
        
        mesh_data_group = LabelFrame(self.parent, text="Mesh data", padx=5, pady=5)
        mesh_data_group.pack(padx=10, pady=5)
        
        current_row = 0
        original_group = LabelFrame(mesh_data_group, text="Orignal Mesh", padx=5, pady=5)
        original_group.grid(row=0, column=0)

        Label(original_group, text="face count:").grid(row=current_row, column=0,sticky=E)
        Label(original_group, textvariable=self.original_face_count_num).grid(row=current_row, column=1,sticky=W)
        current_row = current_row + 1
        Label(original_group, text="vertex count:").grid(row=current_row, column=0,sticky=E)
        Label(original_group, textvariable=self.original_vertex_count_num).grid(row=current_row, column=1,sticky=W)
        
        Label(mesh_data_group, text=" ").grid(row=0, column=1,sticky=E)
        
        current_row = 0
        simplified_group = LabelFrame(mesh_data_group, text="Simplified Mesh", padx=5, pady=5)
        simplified_group.grid(row=0, column=2)

        Label(simplified_group, text="face count:").grid(row=current_row, column=0,sticky=E)
        Label(simplified_group, textvariable=self.simplified_face_count_num).grid(row=current_row, column=1,sticky=W)
        current_row = current_row + 1
        Label(simplified_group, text="vertex count:").grid(row=current_row, column=0,sticky=E)
        Label(simplified_group, textvariable=self.simplified_vertex_count_num).grid(row=current_row, column=1,sticky=W)
        
        
        simplification_group = LabelFrame(self.parent, text="Simplification", padx=5, pady=5)
        simplification_group.pack(padx=10, pady=5)
        
        self.input_text = Entry(simplification_group, width=5)
        self.input_text.grid(row=0, column=0)
        
        button = Button(simplification_group, text="Simplify", command=self.simplify)
        button.grid(row=0, column=1)


    def getScreenSize(self):
        return self.parent.winfo_screenwidth(), self.parent.winfo_screenheight() 

    def select(self):
        self.old_index = self.selected_index
        self.selected_index = self.var.get()
        
    
    def simplify(self):
        text  = self.input_text.get()
        if type(eval(text)) == float and float(text) < 1 and self.selected_index > -1:
            
            if self.simplified_process:
                self.simplified_process.terminate()
                self.simplified_process = None
            
            if self.old_index != self.selected_index:
                self.old_index = self.selected_index
                if self.original_process:
                    self.original_process.terminate()
                    self.original_process = None
             
            fname = self.mesh_list[self.selected_index-1]
            
            original_mesh_width = self.pos[0]
            original_mesh_height = original_mesh_width * 0.75
            original_mesh_x_pos = 0
            original_mesh_y_pos = (self.screen_height - original_mesh_height) / 2
            original_str = " Original\ Mesh " + str(original_mesh_width) + " " + str(original_mesh_height) + " " \
                           + str(original_mesh_x_pos) + " " + str(original_mesh_y_pos)
             
            simplified_mesh_width = original_mesh_width
            simplified_mesh_height = original_mesh_height
            simplified_mesh_x_pos = self.pos[0] + self.window_size[0]
            simplified_mesh_y_pos = original_mesh_y_pos
            simplified_str = " Simplified\ Mesh " + str(simplified_mesh_width) + " " + str(simplified_mesh_height) + " " \
                             + str(simplified_mesh_x_pos) + " " + str(simplified_mesh_y_pos)

            if not self.original_process or self.original_process.poll() is not None:
                
                self.original_process = Popen(load + "./original_mesh/" + fname + original_str, shell=True) # something long running
            
            mesh = Parser.load("./original_mesh/" +fname)
            self.original_face_count_num.set(str(mesh.face_count))
            self.original_vertex_count_num.set(str(mesh.vertex_count))
            
            self.simplifier = Simplification(mesh)
            simplified_mesh = self.simplifier.simplify(float(text))
            
            self.simplified_face_count_num.set(str(simplified_mesh.face_count))
            self.simplified_vertex_count_num.set(str(simplified_mesh.vertex_count))
            
            output = createOutput(fname, self.simplifier, simplified_mesh)
            self.simplifier.printResult()
           
            self.simplified_process = Popen(load + output + simplified_str, shell=True) # something long running
            print "output:", output
            
    def quitHandler(self):
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            if self.simplified_process and self.simplified_process.poll() is None:
                self.simplified_process.terminate()
            if self.original_process and self.original_process.poll() is None:
                self.original_process.terminate()
            root.quit()
 
if __name__ == '__main__':
    root = Tk()
    win = Window(root)
    root.protocol("WM_DELETE_WINDOW", win.quitHandler)
    root.mainloop()
