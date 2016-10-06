import numpy as np
import matplotlib.pyplot as plt
import math

class shm:
    """
        Computes and plots the displacement and velocity of a simple harmonic oscillator over time, using the Euler-Cromer method (please refer to
        http://www.physics.purdue.edu/~hisao/book/www/Computational%20Physics%20using%20MATLAB.pdf).

        Variables:
            Required:
            k: the restring force constant, in kg/s^2
            mass: mass of the oscillator, in kg
            init_pos: initial displacement of the oscillator, in m

            Derived:
            step_size: time for evert tick; default: 0.001
            x: displacement of the oscillator, in m
            v: velocity of the oscillator, in m/s
            a: acceleration, in m/s^2
            t: the ticks
            ke: kinetic energy, in J
            pe: potential energy, in J
            totale: total mechanical energy, in J

            Optional:
            init_v: initial velocity of the oscillator, in m/s; default: 0.0 m/s
            steps: number of ticks; default: 10000
            time: maximum time on the graph, in s; default: 10.0
            b: the damping constant, in kg/s; default: 0.0
            F0: maximum of a periodic driving force, in N; default: 0.0
            drive_freq: angular frequency of the driving force, in rad/s; default: 0.1
    """


    def __init__(self, k, mass, init_pos, init_v = 0.0, steps = 10000, time = 10.0, b = 0.0, F0 = 0.0, drive_freq = 0.1):
        #Configures the essential parameters of the simple harmonic oscillator
        self.k = k
        self.mass = mass
        self.steps = steps
        self.time = time
        self.b = b
        self.F0 = F0
        self.drive_freq = drive_freq

        self.x = np.zeros(self.steps + 1, float)
        self.v = np.zeros(self.steps + 1, float)
        self.a = np.zeros(self.steps + 1, float)
        self.t = np.zeros(self.steps + 1, float)

        self.x[0] = init_pos
        self.v[0] = init_v
        self.t[0] = 0
        self.a[0] = 0


    def computeshm(self):
        #Computes the motion of the simple harmonic oscillator using the Euler-Cromer method:
        self.step_size = self.time / self.steps

        for i in range(1, self.steps + 1):
            self.x[i] = self.x[i - 1] + self.v[i - 1] * self.step_size
            self.v[i] = self.v[i - 1] + (self.F0 * math.cos(self.drive_freq * i * self.step_size) -
                                         self.b * self.v[i - 1] - self.k * self.x[i]) * self.step_size / self.mass
            self.a[i] = (self.v[i] - self.v[i - 1]) / self.step_size
            self.t[i] = self.t[i - 1] + self.step_size

        self.amp = max(self.x)
        self.maxv = max(self.v)
        self.maxa = max(self.a)


    def editshm(self, parameter, value):
        # Edits the value of parameters and the recongifure the shm
        if parameter == "k":
            self.k = value
        elif parameter == "mass":
            self.mass = value
        elif parameter == "steps":
            self.steps = value
        elif parameter == "time":
            self.time = value
        elif parameter == "b":
            self.b = value
        elif parameter == "F0":
            self.F0 = value
        elif parameter == "drive_freq":
            self.drive_freq = value
        elif parameter == "init_pos":
            self.x[0] = value
        elif parameter == "init_v":
            self.v[0] = value
        elif parameter == "step_size":
            self.step_size = value
            self.time = self.step_size * self.steps

        self.computeshm()


    def plotshm(self, yaxis = "x"):
        #Plots the graph of the simple harmonic oscillator
        xvt = []
        xvtlabel = ""
        if yaxis == "x":
            xvt = self.x
            xvtlabel = "Displacement ($m$)"

        elif yaxis == "v":
            xvt = self.v
            xvtlabel = "Velocity ($ms^{-1}$)"

        elif yaxis == "a":
            xvt = self.a
            xvtlabel = "Acceleration ($ms^{-2}$)"

        plt.plot(self.t, xvt)
        plt.xlabel("Time ($s$)")
        plt.ylabel(xvtlabel)
        plt.xlim(0, self.time)
        plt.ylim(min(xvt) * 1.25 - 1, max(xvt) * 1.25 + 1)
        plt.axhspan(min(xvt) * 0.001, max(xvt) * 0.001, color = "black")

        plt.annotate("Maximum " + xvtlabel + ": " + str("{0:.4g}".format(max(xvt))),
                     xy=(self.step_size * np.argmax(xvt), max(xvt)),
                     xytext=(self.step_size * np.argmax(xvt) * 0.55, max(xvt) * 1.15),
                     arrowprops = dict(arrowstyle = "->"))

        plt.annotate("Minimum " + xvtlabel + ": " + str("{0:.4g}".format(min(xvt))),
                     xy=(self.step_size * np.argmin(xvt), min(xvt)),
                     xytext=(self.step_size * np.argmin(xvt) * 0.55, min(xvt) * 1.15),
                     arrowprops=dict(arrowstyle="->"))

        plt.show()


    def compenergy(self):
        #Computes the change in total, kinetic and potential energies
        self.ke = 0.5 * self.mass * (self.v ** 2)
        self.pe = 0.5 * self.k * (self.x ** 2)
        self.totale = self.ke + self.pe

    def plotenergy(self):
        #Plots the change in total, kinetic and potential energies
        self.compenergy()

        noenergy = self.time

        for i in range(self.steps):
            if self.totale[i] <= self.totale[0] * 0.01:
                noenergy = self.t[i]
                break;

        plt.plot(self.t, self.ke, color = "#ffdab3", linewidth = 2)
        plt.plot(self.t, self.totale, color = "#cce6ff", linewidth = 2)
        plt.fill_between(self.t, self.ke, self.totale, facecolor = "#cce6ff", label = "Potential energy")
        plt.fill_between(self.t, 0, self.ke, facecolor = "#ffdab3", label = "Kinetic energy")
        plt.xlabel("Time ($s$)")
        plt.ylabel("Energy ($J$)")
        plt.legend()
        plt.xlim(0, noenergy)
        plt.ylim(self.totale[0] * 0.01, max(self.totale) * 1.15)

        plt.show()








#Wave class under construction as always LUL
"""class wave:

    def __init__(self, v, wl, per):
        #Constructs the wave
        self.v = v
        self.wl = wl
        self.per = v / wl
        self.freq = 1 / self.per

    def configshm(self, shm):
        #If the wave is generated by a simple harmonic oscillator, reconfigure the wave using the shm's parameters
        self.per = shm.per
        self.wl = self.per *

    def c"""



