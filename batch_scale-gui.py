#!/usr/bin/python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE":
# <pieis2pi@u.washington.edu> wrote this file.  As long as you retain this
# notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy me a beer in return.
# -Evan Thomas
# ----------------------------------------------------------------------------

import Tkinter
import tkFileDialog
import glob
import numpy
from stl import mesh

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        self.directory = "."
        self.noclobber = True
        self.firstoctant = True
        self.scale = 1.0
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=1,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set("1.0")

        choosebutton = Tkinter.Button(self,text=u"Choose Directory",
                                command=self.ChooseDirectory)
        choosebutton.grid(column=0,row=0)
        button = Tkinter.Button(self,text=u"Batch Scale",
                                command=self.OnButtonClick)
        button.grid(column=2,row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=2,columnspan=3,sticky='EW')
        self.labelVariable.set(u"Choose a directory and put in a scale factor.")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def ChooseDirectory(self):
        self.directory = tkFileDialog.askdirectory(parent=self.parent, initialdir=".", title='Please select a directory')
        if len(self.directory) > 0:
            self.labelVariable.set(self.directory)
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
        try:
            self.scale=float(self.entryVariable.get())
        except Exception:
            self.labelVariable.set(u"Scale must be a number.")
            return
        for filename in glob.glob(self.directory+"/*.stl"):
            stlmesh = mesh.Mesh.from_file(filename)
            if(self.noclobber):
                bakfilename=filename.rstrip("stl")+"bak"
                stlmesh.save(bakfilename)
            if(self.firstoctant):
                minpoint = [0]*3
                for i in [0,1,2]:
                    minpoint[i]=min(min(stlmesh.v0[:,i]),
                                    min(stlmesh.v1[:,i]),
                                    min(stlmesh.v2[:,i]))
                stlmesh.v0-=minpoint
                stlmesh.v1-=minpoint
                stlmesh.v2-=minpoint
            stlmesh.points*=self.scale
            stlmesh.save(filename)
        self.labelVariable.set("Done!")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Batch STL Scaling Script')
    app.mainloop()
