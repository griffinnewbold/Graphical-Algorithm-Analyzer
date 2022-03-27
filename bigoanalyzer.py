#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.optimize import curve_fit
import sys
import matplotlib.pyplot as plt
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import warnings


os.chdir("/Users/griffin/Downloads")
warnings.filterwarnings('ignore')

root = Tk()
root.title('Big-O Analyzer')
root.geometry('1280x720')
root["bg"] = "silver"



def assignValues():
    return (min_n_entry.get(),max_n_entry.get())


def openC():
    file= filedialog.askopenfile()
    if file is not None:
        content = file.read()
        fp = open('theInput.py', 'w')
        fp.write(content)
        fp.close()
        runFile()
        
        
#handles creation of buttons and attributes
photo = PhotoImage(file = "/Users/griffin/Downloads/button (1).png")
photo2 = PhotoImage(file = "/Users/griffin/Downloads/button.png")
open_file_btn = Button(root,text = "Open File", command=openC, image=photo)
open_file_btn.pack(side=TOP, anchor=N, pady =(10,10))
open_file_btn["border"] = "0"
exit_button = Button(root, text="Exit", command='root.destroy()',image=photo2)
exit_button["border"] = "0"
exit_button.pack(side=BOTTOM,anchor=S, pady=(0,10))
#labels for entering testing data
min_n = Label(root,text ='Minimum N')
max_n = Label(root, text='Maximum N')
 
# using place method we can set the position of label
min_n.place(x=10,y=600)
min_n.config(bg="silver")
min_n_entry = Entry(root)
min_n_entry.place(x=10,y=630)

max_n.place(x=250,y=600)
max_n.config(bg="silver")
max_n_entry = Entry(root)
max_n_entry.place(x=250,y=630)
Button(root, text="Submit", command=assignValues).place(x=200,y=680)



#-------------------------------#

from theInput import inputFunction
colors = ["red", "lightgreen", "black", "gold", "purple"]
labels = ["Linear", "Quadratic", "Exponential", "Log", "Nlogn"]
# O(N).
def Linear(x,a,b):
    
    # Return linear model.
    return a+b*x

# O(N^2).
def Quadratic(x,a,b):
    
    # Return quadratic model.
    return a+b*x**2

# O(M^N).
def Exponential(x,a,b,c):
    
    # Return exponencial model.
    return a+b*2**(c*x)

# O(log(N)).
def Log(x,a,b,c):
    
    # Return log(N) model.
    return a+b*np.log(c*x)

# O(Nlog(N)).
def Nlog(x,a,b):
    
    # Return nlog model.
    return a+x*np.log2(x)

# Fit function
def doFit(function,X,Y,i,plot1):
    
    # Attempt fit.
    try:
        
        # Without initial guesses, exponential might fail.
        if function.__name__=="Exponential":
            
            # Adds good initial guesses.
            popt,pcov=curve_fit(function,X,Y,p0=(2,2,2)) # Fit parameters 
        
        else:
            
            #Other functions can run without initial guess.
            popt,pcov=curve_fit(function,X,Y) # Fit parameters 
        
    # Fit unsuccesful
    except:
        return False,0,0
    
    # Fit sucessful, calculate error and plot.
    r=1-(np.sum((Y-function(X,*popt))**2)/np.sum((Y-np.mean(Y))**2)) # r^2 coefficient.
    plot1.scatter(X,Y,alpha=0.1,color="b")
    plot1.plot(X,function(X,*popt),"g",color=colors[i], label=labels[i])# Plot the fit.
    # Return fit parameters and error.
    return True,popt,r,function.__name__

# Measures the runtime.
def countTime(lower,higher,step):
    
    # Empty arrays to keep measurements.
    X=[]
    Y=[]
    
    # 
    N=lower
    while N<higher:
        
        # Measure the runtime for a given N.
        start=time.perf_counter() # Initial time.
        inputFunction(N) # Run the function.
        end=time.perf_counter() # Final time.
        
        # Record the results and go to the next value.
        X.append(N) # N value.
        Y.append(end-start) # Runtime value. 
        N+=step  # N increment
        
    # Return data points in array format.    
    return np.array(X),np.array(Y)








# Get the measurements.
def runFile():
    assign_tuple = assignValues()
    min_val = int(assign_tuple[0])
    max_val = int(assign_tuple[1])
    if(min_val < 1):
	min_val = 1
    step = (max_val-min_val)/50
    X,Y=countTime(min_val,max_val,step)
    fig = Figure(figsize = (6, 5), dpi = 100)
    plot1 = fig.add_subplot(111)
    list1=[]
            
    list1.append(doFit(Linear,X,Y,0,plot1))
    list1.append(doFit(Quadratic,X,Y,1,plot1))
    list1.append(doFit(Exponential,X,Y,2,plot1))
    list1.append(doFit(Log,X,Y,3,plot1))
    list1.append(doFit(Nlog,X,Y,4,plot1))
    
    plot1.set_ylabel('Time in Seconds')
    plot1.set_xlabel('Size of Input N')
    plot1.legend()
    plot1.axis([min(X),max(X),min(Y),max(Y)])
    

	# creating the Tkinter canvas
	# containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,master = root)
    canvas.draw()

	# placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    list1.sort(key = lambda list1: list1[2])
    list_string = ""
    list1 = list1[::-1]
    
    i = 0
    for element in list1:
        list_string += str(list1[i][3])
        list_string += " : "
        list_string += str(list1[i][2])+"\n"
        i += 1
    print(list_string)
       
    r_value_label = Label(root, text=list_string, bg = 'silver')
    r_value_label.place(x=1005,y=250)
    o_value_label = Label(root, text = "Your code is of: " + list1[0][3] + " order"
                          , bg = 'silver')
    o_value_label.place(x=1020, y=400)
    
#------------------------------#


#main program loop
root.mainloop()
