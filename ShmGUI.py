import numpy as np
import Shm
from tkinter import *
from tkinter import messagebox


class App:
    """
        The main application class of the shm simulator
        Should consist of:
        Variable entry: k, mass, init_pos, init_v, steps, time, b, F0, drive_freq
        The "Compute and plot" button (select from x, v and a)
        The "Compute and plot energy" button
    """

    def __init__(self, master):
        """Configures self"""
        self.master = master
        self.shm = Shm.Shm(0, 0, 0)
        self.genfields()
        self.widgets()

    def genfields(self):
        """Convieniently lists the entry fields"""
        self.fields = np.array([["Force constant", "Mass", "Initial position", "Initial velocity", "Steps",
                                "Total time duration", "Damping constant", "Driving force", "Driving force frequency"],
                               ["k", "mass", "init_pos", "init_v", "steps", "time", "b", "F0", "drive_freq"]])

        self.plotnames = np.array([["Displacement-time", "Velocity-time", "Acceleration-time", "Mechanical energy"],["x", "v", "a", "e"]])

    def genplot(self, threeD=0):
        """Computes shm and generates corresponding plot"""
        self.values = np.arange(9, dtype=float)

        # Pops the error messages
        for i in range(9):
            self.values[i] = float(self.entries[i].get())

            if self.values[i] < 0 and (i is not 2) and (i is not 3) and (i is not 7):
                messagebox.showerror("Error", "Entry value must be non-negative, except for initial position, "
                                              "velocity and driving force.")
                break;

            if self.values[0] == 0 or self.values[1] == 0 or self.values[4] == 0 or self.values[5] == 0:
                messagebox.showerror("Error", "Force constant, Mass, time duration and steps must be positive.")
                break;

        for j in range(9):
            self.shm.edit_shm(self.fields[1, j],self.values[j])

        self.shm.comp_shm()

        if not threeD:
            if self.xvaeplot.get() is not "e":
                self.shm.plot_shm(yaxis=self.xvaeplot.get())
            else:
                self.shm.comp_energy()
                self.shm.plot_energy()
        else:
            self.shm.plot_3d()

    def clear(self):
        """Clears all the data entries"""
        for entry in self.entries:
            entry.delete(0, END)

        for i in range(9):
            if i == 4:
                self.entries[i].insert(0, "10000")
            elif i == 5:
                self.entries[i].insert(0, "10.0")
            else:
                self.entries[i].insert(0, "0")

    def widgets(self):
        """Configures all the widgets"""

        # Title
        self.master.title("Simple Harmonic Motion Simulator")

        # Use iteration to create an array of entry buttons and labels
        self.entries = [0 for x in range(9)]
        self.values = np.zeros(9)

        for i in range(9):
            self.frame1 = Frame(self.master, relief=RIDGE)
            self.frame1.pack(fill=X, padx=5, pady=5)
            self.label = Label(self.frame1, text=self.fields[0, i] + ": ")
            self.label.pack(side=LEFT)
            self.entries[i] = Entry(self.frame1)
            self.entries[i].pack(side=RIGHT)

        self.clear()

        # Radiobutton to select which plot to make
        self.xvaeplot = StringVar()
        self.xvaeplot.set("x")
        self.plot_select = [0 for x in range(4)]

        for i in range(4):
            self.plot_select[i] = Radiobutton(self.master, text=self.plotnames[0, i], variable=self.xvaeplot,
                                             value=self.plotnames[1, i])
            self.plot_select[i].pack(anchor=W)

        # Compute and plot button
        self.comp_plot = Button(self.master, text="Compute and plot", command=lambda: self.genplot())
        self.comp_plot.pack(side=LEFT, padx=5, pady=5)

        # TEST: PLOT 3D GRAPH
        self.threeD_plot = Button(self.master, text="3D plot", command=lambda: self.genplot(1))
        self.threeD_plot.pack(side=LEFT, padx=5, pady=5)

        # Clear entry button
        self.clear_entry = Button(self.master, text="Clear all entries", command=lambda: self.clear())
        self.clear_entry.pack(side=RIGHT, padx=5, pady=5)


        # Clears the plot
        # self.clearplot = Button(self.master, text="Clear plot", command=lambda: self.shm.clearplot())
        # self.clearplot.pack(side=LEFT, padx=5, pady=5)

