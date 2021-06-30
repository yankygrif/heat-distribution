from tkinter import *

import numpy
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation

from itertools import count

import datetime

import random

from scipy.interpolate import Rbf


class main_frame():

    def __init__(self, frame):
        self.frame=frame
        self.path="texttemperature.txt"
        self.data=[]
        self.size=[]
        self.sample=[]
        self.functionsList=["inverse","gaussian","multiquadric",
                            "linear","cubic","quintic",
                            "thin_plate"]
        self.xShift=12
        self.yShift=12

        self.animSpeed=1000

        self.colorMapList=["jet"]
        
        setingsMenu=Menu(frame)
        
        openFileMenu=Menu(setingsMenu, tearoff=1)
        
        openFileMenu.add_command(label="Read from folder")
        openFileMenu.add_command(label="Read from USB")
        
        setingsMenu.add_cascade(label="Open file", menu=openFileMenu)

        self.choosenFunction="inverse"
        
        Button(frame, text="Побудувати графік у реальному часі",
               command=self.surface_temperature).place(relx=0.01, rely=0.24, relwidth=0.5, relheight=0.06)

        Button(frame, text="Побудувати графік нагріву поверхні",
               command=self.surface_by_onesmaple).place(relx=0.01, rely=0.46, relwidth=0.38, relheight=0.06)
        
        Button(frame, text="Відкрити з збереженного файла",
               command=self.open_Read_File).place(relx=0.01,rely=0.30, relwidth=0.5, relheight=0.06)
        
        Button(frame, text="Графік по 5 датчикам",
               command=self.plot_offline).place(relx=0.01,rely=0.37, relwidth=0.5, relheight=0.06)

        self.length=Entry(self.frame)
        self.length.place(relx=0.245,rely=0.54)
        Label(frame, text="Ширина пластини(мм):").place(relx=0.01,rely=0.54)

        self.width=Entry(self.frame)
        self.width.place(relx=0.245,rely=0.62)
        Label(frame, text="Довжина пластини(мм):").place(relx=0.01,rely=0.62)
        
        Button(self.frame, text="Записати", command=self.save_data ).place(relx=0.01,rely=0.81)

        j=0
        
        Label(self.frame, text="Оберіть тип інтерполяції").place(relx=0.61, rely=0.520)


        self.functionsListBox=Listbox(self.frame, selectmode=BROWSE)
        self.functionsListBox.place(relx=0.61, rely=0.60, relheight=0.3)

        for i in self.functionsList:
            self.functionsListBox.insert(j,i)
            j=+1



    def test_com(self):
        print("test")
        
    def surface_temperature(self):
        x_values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y_values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y_values1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y_values2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y_values3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y_values4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        x_stamp =["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]

        index = count()
        def animate(i):
            temp=datetime.datetime.now()
            x_stamp.append(str(temp.hour)+":"+str(temp.minute)+":"+str(temp.second))
            x_values.append(next(index))
            y_values.append(random.randint(15,25))
            y_values1.append(random.
                             randint(25,35))
            y_values2.append(random.randint(35,45))
            y_values3.append(random.randint(45,55))
            y_values4.append(random.randint(55,65))
            plt.cla()
            plt.xticks(x_values, x_stamp)
            plt.axis((x_values[len(x_values)-11],x_values[len(x_values)-1],0,100))
            plt.plot(x_values, y_values)
            plt.plot(x_values, y_values1)
            plt.plot(x_values, y_values2)
            plt.plot(x_values, y_values3)
            plt.plot(x_values, y_values4)
        ani = FuncAnimation( plt.gcf(), animate, 1000, interval=1000)
        plt.tight_layout()
        plt.show()
        
        
    
    def tripleplot_animated(self):
        

        pass
    
    def save_data(self):
        a=int(self.length.get())
        b=int(self.width.get())
        self.choosenFunction=self.functionsListBox.get(self.functionsListBox.curselection())
        self.size=[a,b]
        print(self.size, self.choosenFunction)
        
    def open_Read_File(self):
        file=open(self.path, "r")
        data=file.readlines()
        file.close()
        for i in range(0, len(data)):
            data[i].replace("\t"," ")
            data[i]=data[i].split()
        data=numpy.array(data)
        data=data.astype(numpy.float)
        data=data.T
        self.data=data
        print ("data read completed", data)
        
    def plot_offline(self):
        self.x_data=list()
        plt.ylim(0, 75)
        plt.ylabel("Температура(C)")
        plt.xlabel("Час")
        for i in range(len(self.data[0])):
            self.x_data.append(i*5)
                        
        for i in self.data:
            
            plt.plot(self.x_data, i)


        plt.show()
        
    def surface_by_onesmaple(self):
        
        x = np.array([(self.size[0]/100)*self.xShift,
                      (self.size[0]/100)*self.xShift,
                      self.size[0]-(self.size[0]/100)*self.xShift,
                      self.size[0]-(self.size[0]/100)*self.xShift,
                      self.size[0]/2])
        
        y = np.array([(self.size[0]/100)*self.yShift,
                      self.size[1]-(self.size[0]/100)*self.yShift,
                      self.size[1]-(self.size[0]/100)*self.yShift,
                      (self.size[0]/100)*self.yShift,
                      self.size[1]/2])
        
        a = np.array([21.3, 21.0, 37.0, 35.9, 42.3])
        
        xi, yi = np.mgrid[x.min():x.max():500j, y.min():y.max():500j]
        
        a_rescaled = (a -a.min()) / (a.ptp())
        rbf = Rbf(x, y, a_rescaled, function=self.choosenFunction)
        ai = rbf(xi, yi)
        ai = a.ptp() * ai + a.min()
        
        fig, ax = plt.subplots()
        bnd=matplotlib.colors.Normalize(a.min()-10, a.max()+10)

        im = ax.imshow(ai.T, origin='lower',
                   extent=[0, x.max()+x.min(), 0,
                           y.max()+y.min()], cmap="jet", norm=bnd )
        
        ax.scatter(x, y, c=a)
        
        ax.set(xlabel='X', ylabel='Y', title="Поверхня")

        fig.colorbar(im)

        ax.set_ylabel('Ширина(см)')

        ax.set_xlabel('Довжина(см)')

        for i in range(len(x)):
            text="Датчик "+str(i+1)+"\n"+str(a[i])+" C"
            ax.annotate(text, (x[i], y[i]))
        plt.show()
                
    def surface_by_1000samples(self):
        x = np.array([40, 40, 260, 260, 150])
        y = np.array([40, 110, 110, 40, 75])
        a = np.array([21.3, 21.0, 37.0, 35.9, 42.3])
        xi, yi = np.mgrid[x.min():x.max():500j, y.min():y.max():500j]
        
        a_rescaled = (a -a.min()) / (a.ptp())
        rbf = Rbf(x, y, a_rescaled, function=self.choosenFunction)
        ai = rbf(xi, yi)
        ai = a.ptp() * ai + a.min()
        
        fig, ax = plt.subplots()
        bnd=matplotlib.colors.Normalize(a.min()-10, a.max()+10)

        im = ax.imshow(ai.T, origin='lower',
                   extent=[0, x.max()+x.min(), 0,
                           y.max()+y.min()], cmap="jet", norm=bnd )
        ax.scatter(x, y, c=a)

        ax.set(xlabel='X', ylabel='Y', title="Поверхня")
        fig.colorbar(im)
        ax.set_ylabel('Ширина(см)')
        ax.set_xlabel('Довжина(см)')
        for i in range(len(x)):
            text="Датчик "+str(i+1)+"\n"+str(a[i])+" C"
            ax.annotate(text, (x[i], y[i]))
        plt.show()

        

    
        






root=Tk()
root.resizable(False,False)
root.geometry("600x400")
root.title("ПСНК Лаб5")
MainFrame=main_frame(root)
root.mainloop()

