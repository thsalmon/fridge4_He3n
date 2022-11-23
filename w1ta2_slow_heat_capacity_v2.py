import os
os.chdir(os.path.dirname(__file__))

import sys

from matplotlib import pyplot as plt

sys.path.insert(0, '../exp_py/graphene')

import numpy as np

# import graphene
import graphene
graphene.set_args(['ssh', 'f4a', 'device_c', 'ask', 'db'])
graphene.set_cache('.graphene')

#load a text file of times. t1 column 0, t2 column 1.
times=np.loadtxt('times.txt')

#open some empty lists
heat_capacity=[]
heat_leak=[]
average_temperature=[]
time_1=[]
time_2=[]

#define time_set function
def time_set(t1, t2):
    # set temp and volt to be 30 mins before t1 and 30 mins after t2
    temp=graphene.get_range('w1ta2:f1', t1-30*60, t2+30*60)
    volt=graphene.get_range('volt_h1', t1-30*60, t2+30*60)
    #set t0 as inital time
    t0= temp[0][0]

    # subtract t0 from time:
    temp[0,:] -= t0
    t1 -= t0
    t2 -= t0

    # three ranges: before, during, after heating
    ind1 = np.where(temp[0] < t1)
    ind2 = np.where(np.logical_and(temp[0] >= t1, temp[0] < t2)) 
    ind3 = np.where(temp[0] >= t2)

    #break up the time into 3 parts and subtract initial time to start graph at zero
    time_initial=temp[0][ind1]
    time_centre=temp[0][ind2]
    time_end=temp[0][ind3]
    #break up the temp into 3 parts
    temp_inital=temp[1][ind1]
    temp_centre=temp[1][ind2]
    temp_end=temp[1][ind3]
    
    # plot figure 1
    plt.figure(1)
    plt.clf()
    # polynomial fit of x against y (temp values), 1st order polynomial
    z_initial=np.polyfit(time_initial, temp_inital, 1)
    p_initial = np.poly1d(z_initial)
    # # finds the gradient from the polynomial fit output 
    # print("Grad_initial =", p_initial[1])
    # creates a linspace suitable for the length of the displayed fit line
    xp_initial= np.linspace(0, t1 + 200, 100)
    
    # centre part 
    z_centre=np.polyfit(time_centre, temp_centre, 1)
    p_centre = np.poly1d(z_centre)
    # # finds the gradient from the polynomial fit output 
    # print("Grad_centre =", p_centre[1])
    # creates a linspace suitable for the length of the displayed fit line
    xp_centre = np.linspace(t1 - 100, t2 +200, 100)

    # end part 
    z_end=np.polyfit(time_end, temp_end, 1)
    p_end = np.poly1d(z_end)
    # # finds the gradient from the polynomial fit output 
    # print("Grad_end =", p_end[1])
    # creates a linspace suitable for the length of the displayed fit line
    xp_end = np.linspace(t2, temp[0][-1]-t0+100, 100)
    
    #plot
    plt.plot(temp[0], temp[1], '.', xp_initial, p_initial(xp_initial), xp_centre, p_centre(xp_centre), xp_end, p_end(xp_end))
    plt.title("w1ta at %d" %(t1))
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (mK)")
    plt.savefig('heat_capacity_slow_temp_plot%d.png' %(t1))
    
    plt.figure(2)
    plt.clf()
    plt.plot(volt[0], volt[1], '*-')
    plt.title("w1ta at %d" %(t1))
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.savefig('heat_capacity_slow_volt_plot%d.png' %(t1))

    #temperature rate (gradients). Temp measured in milliKelvin so *e-3 to convert to K
    # parasitic temperature gradient before heating 
    T_p1=p_initial[1]*1e-3
    # parasitic temperature gradient after heating 
    T_p2=p_end[1]*1e-3
    # average parasitic temperature gradient 
    T_p = (T_p1 + T_p2)/2
    # temperature gradient whilst heating 
    T_h = p_centre[1]*1e-3
    # Voltage applied to heater in Volts
    V = 0.02
    # Resistance of the heater in Ohms
    R = 197.1
    #Temp gradient difference
    T_diff = T_h - T_p
    #Heat capacity in J/K
    c = (V**2)/(R*T_diff)
    #Heat leak in Watts 
    Q_p = c*T_p
    #average temperature 
    T_av = np.mean(temp[1])
    
    #need to save values to an array
    heat_capacity.append(c)
    heat_leak.append(Q_p)
    average_temperature.append(T_av)
    time_1.append(t1)
    time_2.append(t2)

    return heat_capacity, heat_leak, average_temperature, time_1, time_2

for index in range(len(times)):
    t1a=times[index,0]
    t2a=times[index,1]
    heat_capacity, heat_leak, average_temperature, time_1, time_2 =time_set(t1a, t2a)

np.savetxt('time1.txt', time_1)
np.savetxt('time2.txt', time_2)
np.savetxt('avtemp.txt', average_temperature)
np.savetxt('heatcapacity.txt', heat_capacity)
np.savetxt('heatleak.txt', heat_leak)

time1=np.loadtxt('time1.txt')
time2=np.loadtxt('time2.txt')
avtemp=np.loadtxt('avtemp.txt')
heatC=np.loadtxt('heatcapacity.txt')
heatQ=np.loadtxt('heatleak.txt')

# fitting for heat capacity vs. temperature plot
z_temp=np.polyfit(avtemp, heatC, 1)
p_temp = np.poly1d(z_temp)
# creates a linspace suitable for the length of the displayed fit line
xp_temp = np.linspace(avtemp[0], avtemp[-1], 100)

plt.figure(3)
plt.clf
plt.plot(avtemp, heatC, '.', xp_temp, p_temp(xp_temp))
plt.title("15 min heating normal He3 at %d" %(time1[0]))
plt.xlabel("Temperature (mK)")
plt.ylabel("Heat Capacity (J/K)")
plt.savefig('Heat_capacity_v_Temperature%d.png' %(time1[0]))
