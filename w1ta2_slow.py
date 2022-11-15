import sys

from matplotlib import pyplot as plt
sys.path.insert(0, '../exp_py/graphene')


import numpy as np

#set the inital time in unix time stamp such that the graph can start from 0 seconds
#t0=1666264400
#t0  15.11819196 + 1666264400 set t0 so that x1-t0 equals zero 
# adjust t0 as now using more data so t0 is shifted backwards t0=1666264415.11819196-300.11819195747375-1200.0
t0 = 1666262915.00000000252625
diff=1666264720-t0
print('diff=',diff)

# import graphene - atm from the local file 
import graphene
graphene.set_args(['ssh', 'f4a', 'device_c', 'ask', 'db'])
graphene.set_cache('.graphene')
def time_set(t1, t2):
    # set temp and volt to be 5 mins before t1 and 9 mins after t2
    #temp=graphene.get_range('w1ta2:f1', t1-5*60, t2+9*60)
    #volt=graphene.get_range('volt_h1', t1-5*60, t2+9*60)
    #expanding data set to see if flat part will fit properly if there's a greater range of data
    temp=graphene.get_range('w1ta2:f1', t1-30*60, t2+30*60)
    volt=graphene.get_range('volt_h1', t1-30*60, t2+30*60)
    print('zero test =',t1-30*60-t0)
    # plot figure 1
    plt.figure(1)
    plt.clf()
    #plt.plot(temp[0]-t0, temp[1])
    # set x1 as the first row of temp
    x1=temp[0]
    # x2 is a clip of the x values so that the fit is only applied to the correct sections of the plot
    # x1 is the array to be clipped between the min and max values required.
    # x2 is the central part
    x2=np.clip(x1, 1666264720, 1666265530)
    #x=temp[0]-t0
    # subtracts inital time from clipped array
    x=x2-t0
    # polynomial fit of x against y (temp values), 1st order polynomial
    z=np.polyfit(x, temp[1], 1)
    print('length x cen', len(x))
    print('length y cen ', len(temp[1]))
    p = np.poly1d(z)
    print("Poly1d =",p)
    # finds the gradient from the polynomial fit output 
    print("Grad =", p[1])
    # creates a linspace suitable for the length of the displayed fit line
    xp = np.linspace(1500, 3000, 100)
    
    # clip x1 for the inital part, xi
    xi=np.clip(x1, t0, 1666264720)
    print("xi=",xi)
    timei=xi-t0
    print('timei=', timei)
    zi=np.polyfit(timei, temp[1], 0)
    print('length=', len(timei))
    print('length y =', len(temp[1]))
    p_i = np.poly1d(zi)
    print("p_i =",p_i)
    # finds the gradient from the polynomial fit output 
    print("Grad =", p_i[1])
    # creates a linspace suitable for the length of the displayed fit line
    xpi = np.linspace(0, 2000, 1000)
    
    #plt.plot(x1-t0, temp[1], '.', xpi, p_i(xpi))
    plt.plot(x1-t0, temp[1], '.', xp, p(xp), xpi, p_i(xpi))
    plt.title("w1ta at 2022-10-20 12:18:35")
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature")
    #plt.savefig('slow1plot%d.png' %(t1))
    plt.savefig('/Users/tinekesalmon/Documents/fridge4_He3n/newslow1plot%d.png' %(t1))
    
    plt.figure(2)
    plt.clf()
    plt.plot(volt[0]-t0, volt[1], '*-')
    plt.title("w1ta at 2022-10-20 12:18:35")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    #plt.savefig('slow2plot%d.png' %(t1))
    plt.savefig('/Users/tinekesalmon/Documents/fridge4_He3n/newslow2plot%d.png' %(t1))

#slow heating. starts 2022-10-20 12:18:35 ends 2022-10-20 12:31:33
#convert time to unix 
import datetime
import time
date_time = datetime.datetime(2022, 10, 20, 12, 18, 35)
print("Given Date:",date_time)
print("UNIX timestamp:",
(time.mktime(date_time.timetuple())))
t1a=time.mktime(date_time.timetuple())

date_time = datetime.datetime(2022, 10, 20, 12, 31, 33)
print("Given Date:",date_time)
print("UNIX timestamp:",
(time.mktime(date_time.timetuple())))
t2a=time.mktime(date_time.timetuple())

print(t1a)
print(t2a)

time_set(t1a, t2a)





'''
#convert unix time 
from datetime import datetime
ts = int('1666358760')
#gives time in UTC timezone 
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
'''